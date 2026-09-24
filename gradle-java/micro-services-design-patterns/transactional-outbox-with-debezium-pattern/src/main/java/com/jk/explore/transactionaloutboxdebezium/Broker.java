package com.jk.explore.transactionaloutboxdebezium;

import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.concurrent.TimeUnit;
import org.apache.kafka.clients.admin.Admin;
import org.apache.kafka.clients.admin.AdminClientConfig;
import org.apache.kafka.clients.admin.NewTopic;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.header.Header;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.testcontainers.DockerClientFactory;
import org.testcontainers.kafka.KafkaContainer;

/**
 * A real Kafka broker, running in a container that this demo starts and stops itself.
 *
 * <p>Kafka keeps messages in a topic, which is a log: a list that is only ever added to. A
 * topic is split into partitions, separate lists that can be read side by side. A message
 * with a key always goes to the same partition as every other message with that key, and
 * within one partition the order is kept. Each message sits at a numbered place in its
 * partition, starting at 0, which Kafka calls the offset.
 *
 * <p>This one runs in KRaft mode, a single node with no ZooKeeper, with a small heap so it
 * fits beside a database on a laptop.
 */
public class Broker implements AutoCloseable {

    /** Kafka 4.3.1, the newest release, as the Apache project's own image. */
    public static final String IMAGE = "apache/kafka:4.3.1";

    /** The topic the shop's order events go to. */
    public static final String TOPIC = "order-events";

    /** The topic has three partitions, so that ordering is a real question. */
    public static final int PARTITIONS = 3;

    /** What to say when there is no container runtime, in words a beginner can act on. */
    public static final String NO_RUNTIME_ADVICE =
            "This demo needs a container runtime, because it starts a real Postgres database and a real Kafka broker.\n"
            + "Start Docker Desktop, or any Docker-compatible runtime, wait until it says it is running, and run ./gradlew run again.";

    /** What to say when the runtime is there but a container will not come up. */
    public static final String WOULD_NOT_START_ADVICE =
            "The Postgres or Kafka container would not start. The images are " + OrdersDatabase.IMAGE + " and " + IMAGE + ".\n"
            + "Check that the container runtime is running, has about 1 GB of memory free and can reach the internet, then run ./gradlew run again.";

    private final KafkaContainer container = new KafkaContainer(IMAGE)
            .withEnv("KAFKA_HEAP_OPTS", "-Xms256m -Xmx256m")
            // Nothing is created by accident: a topic exists only because the demo made it.
            .withEnv("KAFKA_AUTO_CREATE_TOPICS_ENABLE", "false");

    /**
     * True when there is a container runtime this demo can use. Checked before anything
     * starts, so a machine without one gets a sentence rather than a stack trace.
     */
    public static boolean containerRuntimeAvailable() {
        try {
            return DockerClientFactory.instance().isDockerAvailable();
        } catch (Throwable t) {
            return false;
        }
    }

    public void start() {
        container.start();
        try (Admin admin = admin()) {
            admin.createTopics(List.of(new NewTopic(TOPIC, PARTITIONS, (short) 1))).all().get(30, TimeUnit.SECONDS);
        } catch (Exception e) {
            throw new IllegalStateException("could not create topic " + TOPIC, e);
        }
    }

    /** Where the broker is listening, as a host name and the randomly chosen port on this machine. */
    public String address() {
        return container.getBootstrapServers();
    }

    private Admin admin() {
        Properties p = new Properties();
        p.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, address());
        return Admin.create(p);
    }

    /** The next free place in every partition. Kept at the start of an act, so the act reads only what it added. */
    public Map<Integer, Long> mark() {
        try (KafkaConsumer<String, String> consumer = consumer()) {
            Map<Integer, Long> mark = new HashMap<>();
            consumer.endOffsets(partitions()).forEach((tp, end) -> mark.put(tp.partition(), end));
            return mark;
        }
    }

    /** How many messages have arrived since the mark. */
    public int countSince(Map<Integer, Long> mark) {
        Map<Integer, Long> now = mark();
        int count = 0;
        for (int p = 0; p < PARTITIONS; p++) {
            count += (int) (now.get(p) - mark.get(p));
        }
        return count;
    }

    /** Waits until at least this many messages have arrived since the mark. */
    public void waitFor(int wanted, Map<Integer, Long> mark, String what) {
        Poll.until(what, () -> countSince(mark) >= wanted);
    }

    /** Every message since the mark, partition by partition, each partition in its own order. */
    public List<OrderEvent> readSince(Map<Integer, Long> mark) {
        List<OrderEvent> events = new ArrayList<>();
        try (KafkaConsumer<String, String> consumer = consumer()) {
            List<TopicPartition> partitions = partitions();
            consumer.assign(partitions);
            Map<TopicPartition, Long> end = consumer.endOffsets(partitions);
            for (TopicPartition tp : partitions) {
                consumer.seek(tp, mark.get(tp.partition()));
            }
            int wanted = countSince(mark);
            Poll.until("reading " + wanted + " messages back from Kafka", () -> {
                for (ConsumerRecord<String, String> r : consumer.poll(Duration.ofMillis(200))) {
                    if (r.offset() < end.get(new TopicPartition(r.topic(), r.partition()))) {
                        events.add(new OrderEvent(r.partition(), r.offset(), r.key(), header(r, "eventType"), header(r, "id")));
                    }
                }
                return events.size() >= wanted;
            });
        }
        events.sort(Comparator.comparingInt(OrderEvent::partition).thenComparingLong(OrderEvent::place));
        return events;
    }

    private static String header(ConsumerRecord<String, String> r, String name) {
        Header h = r.headers().lastHeader(name);
        return h == null ? null : new String(h.value(), StandardCharsets.UTF_8);
    }

    private List<TopicPartition> partitions() {
        List<TopicPartition> partitions = new ArrayList<>();
        for (int p = 0; p < PARTITIONS; p++) {
            partitions.add(new TopicPartition(TOPIC, p));
        }
        return partitions;
    }

    private KafkaConsumer<String, String> consumer() {
        Properties p = new Properties();
        p.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, address());
        p.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        p.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        p.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false");
        return new KafkaConsumer<>(p);
    }

    @Override
    public void close() {
        container.stop();
    }
}
