package com.jk.explore.competingconsumersrabbitmq;

import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import org.testcontainers.DockerClientFactory;
import org.testcontainers.rabbitmq.RabbitMQContainer;
import org.testcontainers.utility.DockerImageName;

/**
 * A real RabbitMQ broker, running in a container that this demo starts and stops itself.
 *
 * <p>The broker is a separate program. It holds the queue of pick orders and decides which
 * picker is handed which order. Everything the demo shows about how many orders a picker may
 * hold, and about orders coming back when a picker dies, is the broker's doing, not the
 * pickers'.
 *
 * <p>The broker listens inside its container on RabbitMQ's usual port, 5672. Testcontainers
 * maps that to a free port on this machine chosen at random, so two runs, or two builds side
 * by side, never fight over a port. {@link #address()} says which one it picked.
 */
public class Broker implements AutoCloseable {

    /** RabbitMQ 4.3.6, the newest release, in its smaller Alpine Linux build. */
    public static final String IMAGE = "rabbitmq:4.3.6-alpine";

    /** What to say when there is no container runtime, in words a beginner can act on. */
    public static final String NO_RUNTIME_ADVICE =
            "This demo needs a container runtime, because it starts a real RabbitMQ broker.\n"
            + "Start Docker Desktop, or any Docker-compatible runtime, wait until it says it is running, and run ./gradlew run again.";

    /** What to say when the runtime is there but the broker will not come up. */
    public static final String WOULD_NOT_START_ADVICE =
            "The RabbitMQ container would not start. The image is " + IMAGE + ".\n"
            + "Check that the container runtime is running and can reach the internet, then run ./gradlew run again.";

    private final RabbitMQContainer container =
            new RabbitMQContainer(DockerImageName.parse(IMAGE).asCompatibleSubstituteFor("rabbitmq"));

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
        return container.getHost() + ":" + container.getAmqpPort();
    }

    /** One network connection to the broker. Every picker gets its own, as separate programs would. */
    public Connection connect() {
        try {
            ConnectionFactory factory = new ConnectionFactory();
            factory.setUri(container.getAmqpUrl());
            factory.setUsername(container.getAdminUsername());
            factory.setPassword(container.getAdminPassword());
            // The client will quietly reconnect and rebuild everything after a dropped
            // connection unless it is told not to. This demo shows a picker dying, so a
            // dropped connection has to stay dropped.
            factory.setAutomaticRecoveryEnabled(false);
            return factory.newConnection();
        } catch (Exception e) {
            throw new IllegalStateException("could not connect to the broker at " + address(), e);
        }
    }

    @Override
    public void close() {
        container.stop();
    }
}
