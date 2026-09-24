package com.jk.explore.idempotentconsumerkafka;

import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;

/**
 * One running copy of the notifications service, reading the orders topic as a member of a
 * consumer group.
 *
 * <p>The copy asks Kafka for orders, handles each one, and then asks the broker to write
 * down the place it has reached. Kafka calls that writing-down committing the offset. The
 * copy does it by hand, only after the work is done, because that is what makes delivery
 * at least once: if the copy stops before the place is written down, the next copy starts
 * from the old place and is handed the same orders again.
 */
public class Notifications implements AutoCloseable {

    private final String name;
    private final KafkaConsumer<String, String> consumer;
    private final List<Long> placesHandedOver = new ArrayList<>();
    private boolean stopped;

    public Notifications(String name, Broker broker, String group, String topic) {
        this(name, broker, group, topic, Duration.ofMinutes(5));
    }

    /**
     * @param patience how long Kafka lets this copy go without asking for more orders before
     *                 it decides the copy is stuck and hands its orders to another copy.
     *                 Kafka calls it {@code max.poll.interval.ms}; its default is five minutes.
     */
    public Notifications(String name, Broker broker, String group, String topic, Duration patience) {
        this.name = name;
        Properties p = new Properties();
        p.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, broker.address());
        p.put(ConsumerConfig.GROUP_ID_CONFIG, group);
        p.put(ConsumerConfig.CLIENT_ID_CONFIG, name);
        p.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        p.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        // The place is written down by hand, after the work, never on a timer.
        p.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false");
        // A group with no place written down starts at the beginning of the topic.
        p.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        p.put(ConsumerConfig.MAX_POLL_INTERVAL_MS_CONFIG, Long.toString(patience.toMillis()));
        this.consumer = new KafkaConsumer<>(p);
        this.consumer.subscribe(List.of(topic));
    }

    /** Asks Kafka for orders until it has been handed this many. Handles none of them. */
    public List<OrderPlaced> take(int wanted) {
        List<OrderPlaced> taken = new ArrayList<>();
        Poll.until(name + " to be handed " + wanted + " orders", () -> {
            for (ConsumerRecord<String, String> r : consumer.poll(Duration.ofMillis(200))) {
                placesHandedOver.add(r.offset());
                taken.add(OrderPlaced.read(r.value(), Instant.ofEpochMilli(r.timestamp())));
            }
            return taken.size() >= wanted;
        });
        return taken;
    }

    /** Takes this many orders and handles each one. Returns how many emails were queued. */
    public int takeAndHandle(int wanted, Handler handler) {
        int queued = 0;
        for (OrderPlaced order : take(wanted)) {
            if (handler.handle(order)) {
                queued++;
            }
        }
        return queued;
    }

    /** Asks the broker to write down the place this copy has reached. */
    public void sayDone() {
        consumer.commitSync();
    }

    /**
     * The copy stops without writing down its place.
     *
     * <p>It leaves the group politely, so the broker hands its orders on at once. A copy that
     * is killed outright cannot say goodbye, and the broker would first wait for its
     * heartbeat to stop, 45 seconds by default. What the next copy is handed is the same
     * either way.
     */
    public void crash() {
        close();
    }

    /** The places, counting from 0, of every order this copy has been handed. */
    public List<Long> placesHandedOver() {
        return placesHandedOver;
    }

    public String name() {
        return name;
    }

    @Override
    public void close() {
        if (!stopped) {
            stopped = true;
            consumer.close();
        }
    }
}
