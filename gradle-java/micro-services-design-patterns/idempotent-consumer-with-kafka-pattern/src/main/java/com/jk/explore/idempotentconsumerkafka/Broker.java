package com.jk.explore.idempotentconsumerkafka;

import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.concurrent.TimeUnit;
import org.apache.kafka.clients.admin.Admin;
import org.apache.kafka.clients.admin.AdminClientConfig;
import org.apache.kafka.clients.admin.Config;
import org.apache.kafka.clients.admin.NewTopic;
import org.apache.kafka.clients.consumer.OffsetAndMetadata;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.config.ConfigResource;
import org.testcontainers.DockerClientFactory;
import org.testcontainers.kafka.KafkaContainer;

/**
 * A real Kafka broker, running in a container that this demo starts and stops itself.
 *
 * <p>Kafka keeps every order in a topic, which is a log: a list that is only ever added to.
 * Each order sits at a numbered place in that list, starting at 0, and Kafka calls that
 * number the offset. A consumer group is one service, however many copies of it run. The
 * broker writes down, for each group, the place it has reached; the group has to ask for
 * that to be written, and until it does, the broker assumes nothing was handled.
 *
 * <p>This one runs in KRaft mode, a single node with no ZooKeeper, with a small heap so it
 * fits beside a database on a laptop. Testcontainers maps its port to a free one on this
 * machine chosen at random.
 */
public class Broker implements AutoCloseable {

    /** Kafka 4.3.1, the newest release, as the Apache project's own image. */
    public static final String IMAGE = "apache/kafka:4.3.1";

    /** What to say when there is no container runtime, in words a beginner can act on. */
    public static final String NO_RUNTIME_ADVICE =
            "This demo needs a container runtime, because it starts a real Kafka broker and a real Postgres database.\n"
            + "Start Docker Desktop, or any Docker-compatible runtime, wait until it says it is running, and run ./gradlew run again.";

    /** What to say when the runtime is there but a container will not come up. */
    public static final String WOULD_NOT_START_ADVICE =
            "The Kafka or Postgres container would not start. The images are " + IMAGE + " and " + Database.IMAGE + ".\n"
            + "Check that the container runtime is running, has about 1 GB of memory free and can reach the internet, then run ./gradlew run again.";

    private final KafkaContainer container = new KafkaContainer(IMAGE)
            .withEnv("KAFKA_HEAP_OPTS", "-Xms256m -Xmx256m");

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
    }

    /** Where the broker is listening, as a host name and the randomly chosen port on this machine. */
    public String address() {
        return container.getBootstrapServers();
    }

    public Admin admin() {
        Properties p = new Properties();
        p.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, address());
        return Admin.create(p);
    }

    /** A topic with one partition, so the order of the orders is the order of their places. */
    public void createTopic(String topic) {
        try (Admin admin = admin()) {
            admin.createTopics(List.of(new NewTopic(topic, 1, (short) 1))).all().get(30, TimeUnit.SECONDS);
        } catch (Exception e) {
            throw new IllegalStateException("could not create topic " + topic, e);
        }
    }

    /** The place the broker has written down for this group, or -1 if it has written none. */
    public long placeWrittenDown(String group, String topic) {
        TopicPartition partition = new TopicPartition(topic, 0);
        try (Admin admin = admin()) {
            Map<TopicPartition, OffsetAndMetadata> places =
                    admin.listConsumerGroupOffsets(group).partitionsToOffsetAndMetadata().get(30, TimeUnit.SECONDS);
            OffsetAndMetadata place = places.get(partition);
            return place == null ? -1 : place.offset();
        } catch (Exception e) {
            throw new IllegalStateException("could not read the place of group " + group, e);
        }
    }

    /**
     * Moves a group's written-down place back to the start of the topic, so that its next
     * copy reads every order again. This is what an operator does to replay a topic, for
     * instance to rebuild something after a bug; Kafka's own tool calls it resetting offsets.
     * The group must have no copy running.
     */
    public void moveGroupBackToTheStart(String group, String topic) {
        try (Admin admin = admin()) {
            admin.alterConsumerGroupOffsets(group, Map.of(new TopicPartition(topic, 0), new OffsetAndMetadata(0)))
                    .all().get(30, TimeUnit.SECONDS);
        } catch (Exception e) {
            throw new IllegalStateException("could not move group " + group + " back to the start", e);
        }
    }

    /** How long this topic keeps an order before deleting it, in hours, as the broker reports it. */
    public long hoursTheTopicKeepsOrders(String topic) {
        ConfigResource resource = new ConfigResource(ConfigResource.Type.TOPIC, topic);
        try (Admin admin = admin()) {
            Config config = admin.describeConfigs(List.of(resource)).all().get(30, TimeUnit.SECONDS).get(resource);
            long millis = Long.parseLong(config.get("retention.ms").value());
            return TimeUnit.MILLISECONDS.toHours(millis);
        } catch (Exception e) {
            throw new IllegalStateException("could not read how long " + topic + " keeps orders", e);
        }
    }

    @Override
    public void close() {
        container.stop();
    }
}
