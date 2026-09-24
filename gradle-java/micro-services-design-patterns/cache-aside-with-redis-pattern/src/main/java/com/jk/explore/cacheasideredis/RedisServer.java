package com.jk.explore.cacheasideredis;

import org.testcontainers.DockerClientFactory;
import org.testcontainers.containers.Container;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.utility.DockerImageName;
import redis.clients.jedis.ConnectionPoolConfig;
import redis.clients.jedis.RedisClient;

/**
 * A real Redis server, running in a container that this demo starts and stops itself.
 *
 * <p>Redis is a separate program that keeps keys and values in memory and answers over the
 * network. It is not part of the shop. Any program that can reach it sees the same keys, which
 * is the first thing a cache inside the shop's own memory could never offer.
 */
public class RedisServer implements AutoCloseable {

    /** Redis 8.10.2 on Alpine Linux, the newest release at the time this project was written. */
    public static final String IMAGE = "redis:8.10.2-alpine";

    private static final int REDIS_PORT = 6379;

    /** What to say when there is no container runtime, in words a beginner can act on. */
    public static final String NO_RUNTIME_ADVICE =
            "This demo needs a container runtime, because it starts a real Redis server.\n"
            + "Start Docker Desktop, or any Docker-compatible runtime, wait until it says it is running, and run ./gradlew run again.";

    /** What to say when the runtime is there but Redis will not come up. */
    public static final String WOULD_NOT_START_ADVICE =
            "The Redis container would not start. The image is " + IMAGE + ".\n"
            + "Check that the container runtime is running and can reach the internet, then run ./gradlew run again.";

    // Testcontainers maps Redis's port to a free random port on this machine, so several
    // copies of this demo, or other projects using Redis, can run side by side.
    private final GenericContainer<?> container =
            new GenericContainer<>(DockerImageName.parse(IMAGE)).withExposedPorts(REDIS_PORT);

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

    public String host() {
        return container.getHost();
    }

    public int port() {
        return container.getMappedPort(REDIS_PORT);
    }

    /**
     * A new connection to Redis for one shop instance. It keeps a small pool of connections,
     * so that fifty requests at once do not queue behind each other on one.
     */
    public RedisClient connect() {
        ConnectionPoolConfig pool = new ConnectionPoolConfig();
        pool.setMaxTotal(64);
        pool.setMaxIdle(64);
        return RedisClient.builder().hostAndPort(host(), port()).poolConfig(pool).build();
    }

    /**
     * Runs redis-cli, Redis's own command-line program, inside the container. It is a
     * separate program from this one, which is the point: it sees what the shop wrote.
     */
    public String cli(String... command) {
        String[] full = new String[command.length + 1];
        full[0] = "redis-cli";
        System.arraycopy(command, 0, full, 1, command.length);
        try {
            Container.ExecResult result = container.execInContainer(full);
            if (result.getExitCode() != 0) {
                throw new IllegalStateException(String.join(" ", full) + " failed: " + result.getStderr());
            }
            return result.getStdout().trim();
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
