package com.jk.explore.deadletterrabbit;

import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import java.time.Duration;
import java.util.function.BooleanSupplier;
import org.testcontainers.DockerClientFactory;
import org.testcontainers.rabbitmq.RabbitMQContainer;
import org.testcontainers.utility.DockerImageName;

/**
 * A real RabbitMQ broker in a container, started and stopped by the demo itself through Testcontainers.
 * Nothing is installed and nothing is left running: the container goes away when this object is closed.
 */
public class Broker implements AutoCloseable {

    /** The broker image. Pinned, so that every run of this demo talks to the same RabbitMQ. */
    public static final String IMAGE = "rabbitmq:4.3.6-alpine";

    /** What to say when there is no container runtime, in words a beginner can act on. */
    public static final String NO_RUNTIME_ADVICE =
            "This demo runs a real RabbitMQ broker in a container, so it needs a container runtime.\n"
            + "Start Docker Desktop, or another Docker-compatible runtime, wait until it reports running, and run ./gradlew run again.";

    /** What to say when the runtime is there but the broker will not come up. */
    public static final String NO_BROKER_ADVICE =
            "The RabbitMQ container would not start, so this demo cannot run.\n"
            + "Check that Docker is running and that it can fetch the image " + IMAGE + ", then run ./gradlew run again.";

    private RabbitMQContainer container;

    /** True when a container runtime is reachable, so the demo can say something useful instead of failing. */
    public static boolean dockerAvailable() {
        try {
            return DockerClientFactory.instance().isDockerAvailable();
        } catch (Throwable t) {
            return false;
        }
    }

    public void start() {
        container = new RabbitMQContainer(DockerImageName.parse(IMAGE).asCompatibleSubstituteFor("rabbitmq"));
        container.start();
    }

    public Connection connect() throws Exception {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost(container.getHost());
        factory.setPort(container.getAmqpPort());
        factory.setUsername(container.getAdminUsername());
        factory.setPassword(container.getAdminPassword());
        return factory.newConnection();
    }

    /**
     * Waits for something the broker has to do on its own, by asking again until it is true.
     * There is no fixed pause anywhere: the wait ends as soon as the condition holds, and gives up loudly.
     */
    public static void waitUntil(String what, BooleanSupplier condition) {
        waitUntil(what, Duration.ofSeconds(60), condition);
    }

    public static void waitUntil(String what, Duration limit, BooleanSupplier condition) {
        long end = System.nanoTime() + limit.toNanos();
        while (System.nanoTime() < end) {
            if (condition.getAsBoolean()) {
                return;
            }
            try {
                Thread.sleep(25);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
        }
        throw new IllegalStateException("gave up waiting after " + limit.toMillis() + " milliseconds: " + what);
    }

    @Override
    public void close() {
        if (container != null) {
            container.stop();
        }
    }
}
