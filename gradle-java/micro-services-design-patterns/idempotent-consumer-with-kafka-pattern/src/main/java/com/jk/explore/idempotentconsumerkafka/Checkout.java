package com.jk.explore.idempotentconsumerkafka;

import java.time.Instant;
import java.util.Properties;
import java.util.concurrent.TimeUnit;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;

/** The checkout service. It writes one OrderPlaced message to the topic for every order. */
public class Checkout implements AutoCloseable {

    private final String topic;
    private final KafkaProducer<String, String> producer;

    public Checkout(Broker broker, String topic) {
        this.topic = topic;
        Properties p = new Properties();
        p.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, broker.address());
        p.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        p.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        this.producer = new KafkaProducer<>(p);
    }

    /** Places the order and waits for Kafka to say where it wrote it. Returns that place. */
    public long place(OrderPlaced order) {
        return send(new ProducerRecord<>(topic, order.orderId(), order.text()));
    }

    /** Places an order with a time stamp in the past, as if it had been placed back then. */
    public long placeAsOf(OrderPlaced order, Instant placedAt) {
        return send(new ProducerRecord<>(topic, null, placedAt.toEpochMilli(), order.orderId(), order.text()));
    }

    private long send(ProducerRecord<String, String> record) {
        try {
            return producer.send(record).get(30, TimeUnit.SECONDS).offset();
        } catch (Exception e) {
            throw new IllegalStateException("Kafka did not accept " + record.value(), e);
        }
    }

    @Override
    public void close() {
        producer.close();
    }
}
