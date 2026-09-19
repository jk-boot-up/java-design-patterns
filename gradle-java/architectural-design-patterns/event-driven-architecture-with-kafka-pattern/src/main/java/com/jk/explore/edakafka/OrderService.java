package com.jk.explore.edakafka;

import java.util.Properties;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;

/** Accepts an order and tells the log. It does not know who reads the log. */
public class OrderService implements AutoCloseable {

    private final KafkaProducer<String, String> producer;
    private final String topic;

    public OrderService(String topic) {
        this.topic = topic;
        Properties p = new Properties();
        p.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, Broker.SERVERS);
        p.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        p.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        p.put(ProducerConfig.ACKS_CONFIG, "all");
        this.producer = new KafkaProducer<>(p);
    }

    /** Returns the offset that the broker gave the event. */
    public long place(String orderId) throws Exception {
        return producer.send(new ProducerRecord<>(topic, orderId, "OrderPlaced " + orderId)).get().offset();
    }

    @Override
    public void close() {
        producer.close();
    }
}
