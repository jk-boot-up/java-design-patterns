package com.jk.explore.ratelimiterredis;

import io.lettuce.core.RedisClient;
import io.lettuce.core.api.StatefulRedisConnection;
import io.lettuce.core.api.sync.RedisCommands;
import org.testcontainers.DockerClientFactory;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.utility.DockerImageName;

/**
 * A real Redis server, running in a container that this demo starts and stops itself.
 *
 * <p>Redis is a separate program that keeps small values in memory under names, called keys,
 * and lets many programs read and change them over the network. Here it holds one thing: how
 * many searches each client has left. Every shop server asks it, so every shop server sees
 * the same answer.
 */
public class Redis implements AutoCloseable {

    /** Redis 8.10.2 on Alpine Linux, the newest release at the time this project was written. */
    public static final String IMAGE = "redis:8.10.2-alpine";

    /** The port Redis listens on inside the container. Testcontainers maps it to a free one outside. */
    private static final int PORT = 6379;

    /** What to say when there is no container runtime, in words a beginner can act on. */
    public static final String NO_RUNTIME_ADVICE =
            "This demo needs a container runtime, because it starts a real Redis server.\n"
            + "Start Docker Desktop, or any Docker-compatible runtime, wait until it says it is running, and run ./gradlew run again.";

    /** What to say when the runtime is there but Redis will not come up. */
    public static final String WOULD_NOT_START_ADVICE =
            "The Redis container would not start. The image is " + IMAGE + ".\n"
            + "Check that the container runtime is running and can reach the internet, then run ./gradlew run again.";

    private final GenericContainer<?> container =
            new GenericContainer<>(DockerImageName.parse(IMAGE)).withExposedPorts(PORT);

    private RedisClient inspector;
    private StatefulRedisConnection<String, String> inspection;

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
        inspector = RedisClient.create(uri());
        inspection = inspector.connect();
    }

    /** Where Redis is listening, as a URI. The port is a random free one, chosen each run. */
    public String uri() {
        return "redis://" + container.getHost() + ":" + container.getMappedPort(PORT);
    }

    /** Plain commands, for looking at what the shop servers have stored. */
    public RedisCommands<String, String> look() {
        return inspection.sync();
    }

    /** How many keys Redis is holding right now. */
    public long keys() {
        return look().dbsize();
    }

    /** Whole minutes until Redis deletes this key by itself, rounded up. -1 if it never will. */
    public long minutesUntilItForgets(String key) {
        long millis = look().pttl(key);
        if (millis < 0) {
            return -1;
        }
        return (millis + 59_999) / 60_000;
    }

    /** Empties Redis between acts, so each act starts from nothing. */
    public void forgetEverything() {
        look().flushall();
    }

    /** Stops the Redis program. Anything that asks it a question afterwards gets an error. */
    public void stop() {
        if (inspection != null) {
            inspection.close();
            inspector.shutdown();
            inspection = null;
        }
        container.stop();
    }

    public boolean isRunning() {
        return container.isRunning();
    }

    @Override
    public void close() {
        stop();
    }
}
