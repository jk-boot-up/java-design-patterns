package com.jk.explore.messagechannelrabbitmq;

import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import org.testcontainers.DockerClientFactory;
import org.testcontainers.containers.Container;
import org.testcontainers.rabbitmq.RabbitMQContainer;

/**
 * A real RabbitMQ broker, running in a container that this demo starts and stops itself.
 *
 * <p>The broker is a separate program. It is not part of the shop and not part of the
 * warehouse. It sits between them, holds messages, and hands them out. Everything the demo
 * shows about outliving a process, about being told a message was handled, and about
 * surviving a restart is the broker's doing, not the application's.
 */
public class Broker implements AutoCloseable {

    /** RabbitMQ 4.3.6, the newest release at the time this project was written. */
    public static final String IMAGE = "rabbitmq:4.3.6";

    /** What to say when there is no container runtime, in words a beginner can act on. */
    public static final String NO_RUNTIME_ADVICE =
            "This demo needs a container runtime, because it starts a real RabbitMQ broker.\n"
            + "Start Docker Desktop, or any Docker-compatible runtime, wait until it says it is running, and run ./gradlew run again.";

    /** What to say when the runtime is there but the broker will not come up. */
    public static final String WOULD_NOT_START_ADVICE =
            "The RabbitMQ container would not start. The image is " + IMAGE + ".\n"
            + "Check that the container runtime is running and can reach the internet, then run ./gradlew run again.";

    private final RabbitMQContainer container = new RabbitMQContainer(IMAGE);

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

    /** Where the broker is listening, as a host name and a port on this machine. */
    public String address() {
        return container.getHost() + ":" + container.getAmqpPort();
    }

    public Connection connect() {
        try {
            ConnectionFactory factory = new ConnectionFactory();
            factory.setUri(container.getAmqpUrl());
            factory.setUsername(container.getAdminUsername());
            factory.setPassword(container.getAdminPassword());
            // The client will quietly reconnect and rebuild everything after a dropped
            // connection unless it is told not to. This demo shows a receiver dying, so
            // a dropped connection has to stay dropped.
            factory.setAutomaticRecoveryEnabled(false);
            return factory.newConnection();
        } catch (Exception e) {
            throw new IllegalStateException("could not connect to the broker at " + address(), e);
        }
    }

    public Channel channel(String queueName) {
        return new Channel(queueName, connect());
    }

    /**
     * Stops the broker program and starts it again, leaving the container itself alone.
     *
     * <p>This is the closest thing to pulling the plug on the broker that can be done
     * without also moving the port it listens on. Anything the broker was only holding in
     * memory is gone afterwards. Anything it wrote down is still there.
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
            Container.ExecResult result = container.execInContainer(command);
            if (result.getExitCode() != 0) {
                throw new IllegalStateException(String.join(" ", command) + " failed: " + result.getStderr());
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
