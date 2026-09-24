package com.jk.explore.transactionaloutboxdebezium;

import io.debezium.engine.DebeziumEngine;
import io.debezium.engine.RecordChangeEvent;
import io.debezium.engine.format.ChangeEventFormat;
import io.debezium.embedded.Connect;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Comparator;
import java.util.List;
import java.util.Properties;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;
import org.apache.kafka.connect.header.Header;
import org.apache.kafka.connect.source.SourceRecord;

/**
 * Change data capture: Debezium's Postgres connector, run by Debezium's embedded engine
 * inside this program's own JVM, forwarding what it reads to Kafka.
 *
 * <p>Debezium connects to Postgres through a replication slot and is sent every committed
 * change to the {@code outbox} table, straight from Postgres's write-ahead log. Its outbox
 * event router turns each new outbox row into one message: the order id becomes the message
 * key, the payload becomes the message body, the row's id and type become headers, and the
 * topic is {@code order-events}. This class then sends each message to Kafka, and only after
 * Kafka has accepted it does it tell the engine that the change is done. The engine writes
 * down how far it has got in the log in an offsets file, and tells Postgres the same, so the
 * slot can let go of that part of the log. Debezium calls that position the LSN, the log
 * sequence number.
 *
 * <p>Sending first and writing down the position second is what makes delivery at least
 * once. A crash between the two, which {@link #crashAfterSending} arranges, leaves the
 * position behind the messages already sent, and the next start sends them again.
 *
 * <p>Kafka Connect, the usual home for Debezium, runs the same connector and does the same
 * forwarding in its own process. The embedded engine does it here, with no third container.
 */
public class ChangeDataCapture implements AutoCloseable {

    /** The replication slot's name: Postgres's bookmark for this reader. */
    public static final String SLOT = "orders_outbox";

    /** Debezium 3.6.3.Final, the newest generally available release. */
    public static final String DEBEZIUM_VERSION = "3.6.3.Final";

    private final OrdersDatabase database;
    private final KafkaProducer<String, String> producer;
    private final Path offsets;
    private final AtomicInteger sent = new AtomicInteger();
    private volatile int dieWhenSentReaches = Integer.MAX_VALUE;
    private volatile boolean finished = true;
    private DebeziumEngine<RecordChangeEvent<SourceRecord>> engine;
    private ExecutorService thread;

    public ChangeDataCapture(OrdersDatabase database, Broker broker) {
        this.database = database;
        Properties p = new Properties();
        p.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, broker.address());
        p.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        p.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        this.producer = new KafkaProducer<>(p);
        try {
            this.offsets = Files.createTempDirectory("outbox-debezium-offsets").resolve("offsets.dat");
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    private Properties settings() {
        Properties p = new Properties();
        p.setProperty("name", "orders-outbox");
        p.setProperty("connector.class", "io.debezium.connector.postgresql.PostgresConnector");
        // Where the engine writes down how far it has read. Written after every batch.
        p.setProperty("offset.storage", "org.apache.kafka.connect.storage.FileOffsetBackingStore");
        p.setProperty("offset.storage.file.filename", offsets.toString());
        p.setProperty("offset.flush.interval.ms", "0");
        p.setProperty("database.hostname", database.host());
        p.setProperty("database.port", Integer.toString(database.port()));
        p.setProperty("database.user", database.user());
        p.setProperty("database.password", database.password());
        p.setProperty("database.dbname", database.databaseName());
        p.setProperty("topic.prefix", "shop");
        // pgoutput is the decoder built into Postgres; nothing to install in the database.
        p.setProperty("plugin.name", "pgoutput");
        p.setProperty("slot.name", SLOT);
        p.setProperty("publication.name", "orders_outbox");
        p.setProperty("publication.autocreate.mode", "filtered");
        p.setProperty("table.include.list", "public.outbox");
        // Read only what changes from now on; do not copy what the table already holds.
        p.setProperty("snapshot.mode", "no_data");
        p.setProperty("tombstones.on.delete", "false");
        // The outbox event router: one outbox row in, one order event out.
        p.setProperty("transforms", "outbox");
        p.setProperty("transforms.outbox.type", "io.debezium.transforms.outbox.EventRouter");
        p.setProperty("transforms.outbox.route.topic.replacement", Broker.TOPIC);
        p.setProperty("transforms.outbox.table.fields.additional.placement", "type:header:eventType");
        return p;
    }

    /** Starts the engine and waits until it is connected to the slot and reading. */
    public void start() {
        finished = false;
        engine = DebeziumEngine.create(ChangeEventFormat.of(Connect.class))
                .using(settings())
                .using((success, message, error) -> finished = true)
                .notifying(this::handleBatch)
                .build();
        thread = Executors.newSingleThreadExecutor(r -> {
            Thread t = new Thread(r, "debezium-engine");
            t.setDaemon(true);
            return t;
        });
        thread.execute(engine);
        Poll.until("Debezium to connect to the replication slot", () -> database.slotActive(SLOT));
    }

    private void handleBatch(List<RecordChangeEvent<SourceRecord>> records,
                             DebeziumEngine.RecordCommitter<RecordChangeEvent<SourceRecord>> committer)
            throws InterruptedException {
        boolean crashing = dieWhenSentReaches != Integer.MAX_VALUE;
        for (RecordChangeEvent<SourceRecord> event : records) {
            SourceRecord r = event.record();
            if (r.value() != null) {
                send(r);
                if (sent.incrementAndGet() >= dieWhenSentReaches) {
                    throw new ProcessDied("after sending to Kafka, before writing down its position");
                }
            }
            if (!crashing) {
                committer.markProcessed(event);
            }
        }
        if (!crashing) {
            committer.markBatchFinished();
        }
    }

    private void send(SourceRecord r) {
        ProducerRecord<String, String> record =
                new ProducerRecord<>(r.topic(), r.key() == null ? null : r.key().toString(), r.value().toString());
        for (Header h : r.headers()) {
            record.headers().add(h.key(), String.valueOf(h.value()).getBytes(StandardCharsets.UTF_8));
        }
        try {
            producer.send(record).get(30, TimeUnit.SECONDS);
        } catch (Exception e) {
            throw new IllegalStateException("Kafka did not accept an event", e);
        }
    }

    /** How many messages this engine has sent to Kafka since it was made. */
    public int sent() {
        return sent.get();
    }

    /**
     * From now on the engine writes nothing down, and after sending this many more messages
     * the process dies. Waits until it has.
     */
    public void crashAfterSending(int more) {
        dieWhenSentReaches = sent.get() + more;
    }

    /** Waits for the crash arranged by {@link #crashAfterSending} to happen, then clears up. */
    public void awaitCrash() {
        Poll.until("Debezium to die after sending", () -> finished);
        dieWhenSentReaches = Integer.MAX_VALUE;
        shutDown();
    }

    /** Stops the engine the polite way: it writes down its position and lets go of the slot. */
    public void stop() {
        shutDown();
        Poll.until("the replication slot to be released", () -> !database.slotActive(SLOT));
    }

    public boolean running() {
        return !finished;
    }

    private void shutDown() {
        try {
            if (engine != null && !finished) {
                engine.close();
            }
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        } catch (IllegalStateException alreadyShutDown) {
            // the engine stopped itself after the crash; there is nothing left to close
        }
        Poll.until("the Debezium engine to finish", () -> finished);
        thread.shutdown();
        engine = null;
    }

    @Override
    public void close() {
        if (engine != null) {
            shutDown();
        }
        producer.close();
        try {
            Files.deleteIfExists(offsets);
            Files.deleteIfExists(offsets.getParent());
        } catch (IOException ignored) {
            // a temporary file; the operating system clears it in the end
        }
    }
}
