package com.jk.explore.pubsubredis;

import org.testcontainers.DockerClientFactory;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.containers.wait.strategy.Wait;
import org.testcontainers.utility.DockerImageName;
import redis.clients.jedis.Jedis;

/**
 * A real Redis server, running in a container that this demo starts and stops itself.
 *
 * <p>Redis is a separate program. It is not part of the order service and not part of any
 * subscriber. Every subscriber holds its own network connection to it, and when the order
 * service publishes, it is Redis that copies the message down each of those connections. The
 * count it hands back, the limit it keeps on each listener, and the fact that it keeps
 * nothing afterwards are all the server's doing, not the application's.
 */
public class RedisServer implements AutoCloseable {

    /** Redis 8.10.2 on Alpine Linux, the newest release at the time this project was written. */
    public static final String IMAGE = "redis:8.10.2-alpine";

    /** The port Redis listens on inside the container. The demo reaches it on a random free port. */
    private static final int REDIS_PORT = 6379;

    /** What to say when there is no container runtime, in words a beginner can act on. */
    public static final String NO_RUNTIME_ADVICE =
            "This demo needs a container runtime, because it starts a real Redis server.\n"
            + "Start Docker Desktop, or any Docker-compatible runtime, wait until it says it is running, and run ./gradlew run again.";

    /** What to say when the runtime is there but Redis will not come up. */
    public static final String WOULD_NOT_START_ADVICE =
            "The Redis container would not start. The image is " + IMAGE + ".\n"
            + "Check that the container runtime is running and can reach the internet, then run ./gradlew run again.";

    @SuppressWarnings("resource") // closed in close()
    private final GenericContainer<?> container = new GenericContainer<>(DockerImageName.parse(IMAGE))
            .withExposedPorts(REDIS_PORT)
            .waitingFor(Wait.forLogMessage(".*Ready to accept connections.*\\n", 1));

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

    /** The port on this machine that leads to Redis. Testcontainers picks a free one each run. */
    public int port() {
        return container.getMappedPort(REDIS_PORT);
    }

    /** A fresh connection of its own, as a separate service would have. */
    public Jedis connect() {
        return new Jedis(host(), port());
    }

    /**
     * Sets the size limit on the pile of messages Redis will hold for one listener that has
     * not read them yet. Past the limit, Redis closes that listener's connection.
     *
     * <p>Redis's own word for the pile is the client output buffer. Out of the box a
     * listener may fall 32 megabytes behind before it is cut off; the demo lowers that so the
     * point arrives in a few seconds rather than a few minutes. The rule is the same.
     */
    public void limitEachListenerTo(String size) {
        try (Jedis admin = connect()) {
            admin.configSet("client-output-buffer-limit", "pubsub " + size + " 0 0");
        }
    }

    /**
     * The limit Redis is running with, in words: a hard size, and a softer size that is
     * allowed for a number of seconds. Out of the box that is 32mb, or 8mb for 60 seconds.
     */
    public String listenerLimit() {
        try (Jedis admin = connect()) {
            String all = admin.configGet("client-output-buffer-limit").get("client-output-buffer-limit");
            String[] parts = all.substring(all.indexOf("pubsub ")).split(" ");
            return megabytes(parts[1]) + ", or " + megabytes(parts[2]) + " for " + parts[3] + " seconds";
        }
    }

    private static String megabytes(String bytes) {
        return Long.parseLong(bytes) / (1024 * 1024) + "mb";
    }

    /**
     * How many listeners Redis has cut off for falling too far behind, since it started. This
     * is Redis's own count, read from the stats section of INFO.
     */
    public long listenersCutOff() {
        return stat("client_output_buffer_limit_disconnections");
    }

    /** How many listeners Redis has for one channel name, right now. */
    public long listenersOn(String channel) {
        try (Jedis admin = connect()) {
            return admin.pubsubNumSub(channel).get(channel);
        }
    }

    /** How many keys Redis has stored. Publishing never stores one. */
    public long keysStored() {
        try (Jedis admin = connect()) {
            return admin.dbSize();
        }
    }

    /** Starts every count over, so one act's figures do not leak into the next. */
    public void resetCounts() {
        try (Jedis admin = connect()) {
            admin.configResetStat();
        }
    }

    private long stat(String name) {
        try (Jedis admin = connect()) {
            for (String line : admin.info().split("\r?\n")) {
                if (line.startsWith(name + ":")) {
                    return Long.parseLong(line.substring(name.length() + 1).trim());
                }
            }
        }
        throw new IllegalStateException("Redis did not report " + name);
    }

    @Override
    public void close() {
        container.stop();
    }
}
