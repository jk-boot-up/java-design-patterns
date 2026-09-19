package com.jk.explore.edakafka;

import java.time.Duration;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;
import java.util.function.Consumer;
import org.apache.kafka.clients.admin.Admin;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.consumer.OffsetAndMetadata;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.serialization.StringDeserializer;

/**
 * One service reading the topic, as a consumer group of its own. The broker remembers how far the group
 * has read. The reader can be closed, which is a service that is down, and opened again where it left off.
 */
public class Reader implements AutoCloseable {

    private final String group;
    private final String topic;
    private final TopicPartition partition;
    private final boolean idempotent;
    private final Consumer<String> reaction;
    private final Set<Long> seen = new HashSet<>();
    private final KafkaConsumer<String, String> consumer;

    public Reader(String group, String topic, boolean fromStart, boolean idempotent, Consumer<String> reaction) {
        this.group = group;
        this.topic = topic;
        this.partition = new TopicPartition(topic, 0);
        this.idempotent = idempotent;
        this.reaction = reaction;
        Properties p = new Properties();
        p.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, Broker.SERVERS);
        p.put(ConsumerConfig.GROUP_ID_CONFIG, group);
        p.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        p.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        p.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false");
        p.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, fromStart ? "earliest" : "latest");
        this.consumer = new KafkaConsumer<>(p);
        this.consumer.assign(List.of(partition));
    }

    /** Reads until it has been given the wanted number of events, then commits how far it got. Returns how many it reacted to. */
    public int read(int wanted) {
        int received = 0;
        int reacted = 0;
        long end = System.nanoTime() + Duration.ofSeconds(60).toNanos();
        while (received < wanted && System.nanoTime() < end) {
            for (ConsumerRecord<String, String> r : consumer.poll(Duration.ofMillis(500))) {
                received++;
                if (idempotent && !seen.add(r.offset())) {
                    continue;
                }
                reaction.accept(r.value());
                reacted++;
            }
        }
        consumer.commitSync();
        return reacted;
    }

    /** Reads what is there and then goes back to the start and reads it again: a redelivery. */
    public void goBackTo(long offset) {
        consumer.seek(partition, offset);
    }

    /** Where the reader will read next. */
    public long position() {
        return consumer.position(partition);
    }

    /** How many events the topic has that this group has not yet committed past. */
    public static long lag(String group, String topic) throws Exception {
        TopicPartition tp = new TopicPartition(topic, 0);
        try (Admin admin = Broker.admin()) {
            long end = admin.listOffsets(Map.of(tp, org.apache.kafka.clients.admin.OffsetSpec.latest())).all().get().get(tp).offset();
            Map<TopicPartition, OffsetAndMetadata> committed = admin.listConsumerGroupOffsets(group).partitionsToOffsetAndMetadata().get();
            long done = committed.containsKey(tp) ? committed.get(tp).offset() : 0;
            return end - done;
        }
    }

    public String group() {
        return group;
    }

    @Override
    public void close() {
        consumer.close();
    }
}
