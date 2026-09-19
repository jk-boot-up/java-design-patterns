package com.jk.explore.edakafka;

import java.time.Duration;
import java.util.Properties;
import java.util.function.BooleanSupplier;
import org.apache.kafka.clients.admin.Admin;
import org.apache.kafka.clients.admin.AdminClientConfig;
import org.apache.kafka.clients.admin.NewTopic;

/** A real Kafka broker in a Docker container, in KRaft mode: one node, no ZooKeeper. */
public class Broker implements AutoCloseable {

    public static final String IMAGE = "apache/kafka:4.3.1";
    public static final String SERVERS = "127.0.0.1:9092";
    private static final String CONTAINER = "patterns-kafka";

    public static boolean toolsAvailable() {
        return Shell.works("docker", "info") && (Shell.works("docker", "image", "inspect", IMAGE) || Shell.works("docker", "pull", "-q", IMAGE));
    }

    public void start() {
        Shell.works("docker", "rm", "-f", CONTAINER);
        Shell.run("docker", "run", "-d", "--rm", "--name", CONTAINER, "-p", "127.0.0.1:9092:9092", IMAGE);
        waitUntil(() -> {
            try (Admin admin = admin()) {
                admin.listTopics().names().get(3, java.util.concurrent.TimeUnit.SECONDS);
                return true;
            } catch (Exception e) {
                return false;
            }
        });
    }

    public static Admin admin() {
        Properties p = new Properties();
        p.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, SERVERS);
        p.put(AdminClientConfig.REQUEST_TIMEOUT_MS_CONFIG, "5000");
        return Admin.create(p);
    }

    /** A topic with one partition, so that the order of events is the order of offsets. */
    public void createTopic(String name) throws Exception {
        try (Admin admin = admin()) {
            admin.createTopics(java.util.List.of(new NewTopic(name, 1, (short) 1))).all().get();
        }
    }

    public static void waitUntil(BooleanSupplier condition) {
        long end = System.nanoTime() + Duration.ofSeconds(90).toNanos();
        while (System.nanoTime() < end) {
            if (condition.getAsBoolean()) {
                return;
            }
            try {
                Thread.sleep(200);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
        }
        throw new IllegalStateException("Kafka did not settle in 90 seconds");
    }

    @Override
    public void close() {
        Shell.works("docker", "rm", "-f", CONTAINER);
    }
}
