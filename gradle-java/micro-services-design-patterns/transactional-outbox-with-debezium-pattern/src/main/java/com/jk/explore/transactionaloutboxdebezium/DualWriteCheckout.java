package com.jk.explore.transactionaloutboxdebezium;

import java.nio.charset.StandardCharsets;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.Properties;
import java.util.concurrent.TimeUnit;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;

/**
 * The checkout everybody writes first: save the order in Postgres, then send the event to
 * Kafka. Two systems, two separate steps, and nothing that covers both.
 */
public class DualWriteCheckout implements AutoCloseable {

    private final OrdersDatabase database;
    private final KafkaProducer<String, String> producer;

    public DualWriteCheckout(OrdersDatabase database, Broker broker) {
        this.database = database;
        Properties p = new Properties();
        p.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, broker.address());
        p.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        p.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        this.producer = new KafkaProducer<>(p);
    }

    /** Saves, then sends. With {@code dieBetween}, the process dies after the save has committed. */
    public void saveThenSend(Order order, boolean dieBetween) {
        save(order);
        if (dieBetween) {
            throw new ProcessDied("after saving the order, before sending the event");
        }
        send(order);
    }

    /** The two lines swapped: sends, then saves. With {@code dieBetween}, the save never happens. */
    public void sendThenSave(Order order, boolean dieBetween) {
        send(order);
        if (dieBetween) {
            throw new ProcessDied("after sending the event, before saving the order");
        }
        save(order);
    }

    private void save(Order order) {
        try (Connection c = database.connect();
             PreparedStatement s = c.prepareStatement("insert into orders values (?, ?, ?, 'placed')")) {
            s.setString(1, order.orderId());
            s.setString(2, order.customer());
            s.setLong(3, order.totalPence());
            s.executeUpdate();
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }

    private void send(Order order) {
        ProducerRecord<String, String> record = new ProducerRecord<>(Broker.TOPIC, order.orderId(), order.asJson());
        record.headers().add("eventType", "OrderPlaced".getBytes(StandardCharsets.UTF_8));
        record.headers().add("id", OutboxCheckout.eventId(order.orderId(), "OrderPlaced").getBytes(StandardCharsets.UTF_8));
        try {
            producer.send(record).get(30, TimeUnit.SECONDS);
        } catch (Exception e) {
            throw new IllegalStateException("Kafka did not accept the event for " + order.orderId(), e);
        }
    }

    @Override
    public void close() {
        producer.close();
    }
}
