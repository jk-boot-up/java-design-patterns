package com.jk.explore.ecstkafka;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import org.apache.kafka.clients.admin.Admin;
import org.apache.kafka.clients.admin.NewTopic;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.testcontainers.DockerClientFactory;
import org.testcontainers.kafka.KafkaContainer;

/**
 * A real Kafka broker, running in a container that this demo starts and stops itself, with the few
 * operations the demo needs: create a topic, send keyed events, and read a topic from the start.
 */
public final class Kafka implements AutoCloseable {

    /** Apache Kafka 4.3.1, pinned so two runs on two machines use the same broker. */
    public static final String IMAGE = "apache/kafka:4.3.1";

    public static final String NO_RUNTIME_ADVICE =
            "This demo needs a container runtime, because it starts a real Kafka broker.\n"
            + "Start Docker Desktop, or any Docker-compatible runtime, wait until it says it is running, and run ./gradlew run again.";

    public static final String WOULD_NOT_START_ADVICE =
            "The Kafka container would not start. The image is " + IMAGE + ".\n"
            + "Check that the container runtime is running and can reach the internet, then run ./gradlew run again.";

    private final KafkaContainer container = new KafkaContainer(IMAGE);
    private KafkaProducer<String, String> producer;

    public static boolean containerRuntimeAvailable() {
        try {
            return DockerClientFactory.instance().isDockerAvailable();
        } catch (Throwable t) {
            return false;
        }
    }

    public void start() {
        container.start();
        Properties p = new Properties();
        p.put("bootstrap.servers", container.getBootstrapServers());
        p.put("key.serializer", StringSerializer.class.getName());
        p.put("value.serializer", StringSerializer.class.getName());
        p.put("acks", "all");
        producer = new KafkaProducer<>(p);
    }

    /** A topic with {@code partitions}; compacted topics keep at least the latest event for every key. */
    public void createTopic(String name, int partitions, boolean compacted) throws Exception {
        try (Admin admin = Admin.create(Map.of("bootstrap.servers", container.getBootstrapServers()))) {
            NewTopic t = new NewTopic(name, partitions, (short) 1);
            if (compacted) {
                t.configs(Map.of("cleanup.policy", "compact"));
            }
            admin.createTopics(List.of(t)).all().get();
        }
    }

    /** Sends an event and waits until the broker has stored it. A null value is a tombstone. */
    public void send(String topic, String key, String value) throws Exception {
        producer.send(new ProducerRecord<>(topic, key, value)).get();
    }

    /** Sends an event to one chosen partition, to show what keys normally prevent. */
    public void sendToPartition(String topic, int partition, String key, String value) throws Exception {
        producer.send(new ProducerRecord<>(topic, partition, key, value)).get();
    }

    /**
     * Reads every event now in the topic, from the beginning, partition by partition in the order given,
     * and stops when it has caught up. This is what a new copy does when it first starts.
     */
    public List<ConsumerRecord<String, String>> readAll(String topic, List<Integer> partitionOrder) {
        Properties p = new Properties();
        p.put("bootstrap.servers", container.getBootstrapServers());
        p.put("key.deserializer", StringDeserializer.class.getName());
        p.put("value.deserializer", StringDeserializer.class.getName());
        p.put("enable.auto.commit", "false");
        List<ConsumerRecord<String, String>> out = new ArrayList<>();
        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(p)) {
            for (int partition : partitionOrder) {
                TopicPartition tp = new TopicPartition(topic, partition);
                consumer.assign(List.of(tp));
                consumer.seekToBeginning(List.of(tp));
                long end = consumer.endOffsets(List.of(tp)).get(tp);
                long deadline = System.currentTimeMillis() + 30_000;
                while (consumer.position(tp) < end && System.currentTimeMillis() < deadline) {
                    consumer.poll(Duration.ofMillis(200)).forEach(out::add);
                }
            }
        }
        return out;
    }

    @Override
    public void close() {
        if (producer != null) {
            producer.close();
        }
        container.stop();
    }
}
