package com.jk.explore.guaranteedrabbit;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import org.testcontainers.DockerClientFactory;
import org.testcontainers.containers.Container;
import org.testcontainers.rabbitmq.RabbitMQContainer;

/**
 * A real RabbitMQ broker, running in a container that this demo starts and stops itself.
 *
 * <p>The broker is a separate program that holds messages between the shop and the email sender.
 * Whether a message survives a restart is decided here, by how the queue and the message were
 * declared, not by the shop's code.
 */
public final class Broker implements AutoCloseable {

    /** RabbitMQ 4.3.6, pinned so two runs on two machines use the same broker. */
    public static final String IMAGE = "rabbitmq:4.3.6";

    public static final String NO_RUNTIME_ADVICE =
            "This demo needs a container runtime, because it starts a real RabbitMQ broker.\n"
            + "Start Docker Desktop, or any Docker-compatible runtime, wait until it says it is running, and run ./gradlew run again.";

    public static final String WOULD_NOT_START_ADVICE =
            "The RabbitMQ container would not start. The image is " + IMAGE + ".\n"
            + "Check that the container runtime is running and can reach the internet, then run ./gradlew run again.";

    private final RabbitMQContainer container = new RabbitMQContainer(IMAGE);

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

    public Connection connect() {
        try {
            ConnectionFactory factory = new ConnectionFactory();
            factory.setUri(container.getAmqpUrl());
            factory.setUsername(container.getAdminUsername());
            factory.setPassword(container.getAdminPassword());
            factory.setAutomaticRecoveryEnabled(false);   // a dropped connection must stay dropped
            return factory.newConnection();
        } catch (Exception e) {
            throw new IllegalStateException("could not connect to the broker", e);
        }
    }

    /** How many messages are waiting in a queue, or -1 if the queue no longer exists. */
    public int waiting(String queue) {
        try (Connection c = connect(); Channel ch = c.createChannel()) {
            return ch.queueDeclarePassive(queue).getMessageCount();
        } catch (Exception e) {
            return -1;
        }
    }

    /**
     * Stops the broker program and starts it again inside the same container: everything it held only
     * in memory is gone; everything it wrote to disk is still there.
     */
    public void restart() {
        exec("rabbitmqctl", "stop_app");
        exec("rabbitmqctl", "start_app");
        Poll.until("the broker to accept connections again", () -> {
            try (Connection ignored = connect()) {
                return true;
            } catch (Exception e) {
                return false;
            }
        });
    }

    private void exec(String... command) {
        try {
            Container.ExecResult r = container.execInContainer(command);
            if (r.getExitCode() != 0) {
                throw new IllegalStateException(String.join(" ", command) + " failed: " + r.getStderr());
            }
        } catch (RuntimeException e) {
            throw e;
        } catch (Exception e) {
            throw new IllegalStateException(e);
        }
    }

    @Override
    public void close() {
        container.stop();
    }
}
