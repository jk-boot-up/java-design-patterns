package com.jk.explore.eventbusnats;

import java.time.Duration;
import org.testcontainers.DockerClientFactory;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.containers.wait.strategy.Wait;
import org.testcontainers.utility.DockerImageName;

/**
 * A real NATS server in a container, started and stopped by the demo itself.
 *
 * <p>NATS is a message bus that runs as a program of its own. It keeps nothing: an event it is given is
 * handed to whoever is listening at that instant, and then forgotten. The container also opens a second
 * port for monitoring, which is how a question such as "how many listeners are there" can be asked at all.
 */
public class NatsServer implements AutoCloseable {

    public static final String IMAGE = "nats:2.15.0-alpine";

    private static final int CLIENT_PORT = 4222;
    private static final int MONITOR_PORT = 8222;

    private final GenericContainer<?> container = new GenericContainer<>(DockerImageName.parse(IMAGE))
            .withExposedPorts(CLIENT_PORT, MONITOR_PORT)
            .withCommand("--http_port", String.valueOf(MONITOR_PORT))
            .waitingFor(Wait.forHttp("/healthz").forPort(MONITOR_PORT).forStatusCode(200)
                    .withStartupTimeout(Duration.ofMinutes(3)));

    /** True when there is a container runtime this demo can use. */
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

    /** Where a client connects to publish and to subscribe. */
    public String url() {
        return "nats://" + container.getHost() + ":" + container.getMappedPort(CLIENT_PORT);
    }

    /** Where the server answers questions about itself. */
    public String monitorUrl() {
        return "http://" + container.getHost() + ":" + container.getMappedPort(MONITOR_PORT);
    }

    @Override
    public void close() {
        container.stop();
    }
}
