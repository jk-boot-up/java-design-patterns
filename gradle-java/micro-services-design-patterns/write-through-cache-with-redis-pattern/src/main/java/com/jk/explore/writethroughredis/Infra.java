package com.jk.explore.writethroughredis;

import java.sql.Connection;
import java.sql.DriverManager;
import org.testcontainers.DockerClientFactory;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.postgresql.PostgreSQLContainer;
import redis.clients.jedis.DefaultJedisClientConfig;
import redis.clients.jedis.HostAndPort;
import redis.clients.jedis.Jedis;

/**
 * A real Redis and a real PostgreSQL, each in a container that this demo starts and stops itself.
 */
public final class Infra implements AutoCloseable {

    public static final String REDIS_IMAGE = "redis:8.10.2-alpine";
    public static final String POSTGRES_IMAGE = "postgres:18.6-alpine";

    public static final String NO_RUNTIME_ADVICE =
            "This demo needs a container runtime, because it starts a real Redis and a real PostgreSQL.\n"
            + "Start Docker Desktop, or any Docker-compatible runtime, wait until it says it is running, and run ./gradlew run again.";

    public static final String WOULD_NOT_START_ADVICE =
            "The Redis or PostgreSQL container would not start. The images are " + REDIS_IMAGE + " and " + POSTGRES_IMAGE + ".\n"
            + "Check that the container runtime is running and can reach the internet, then run ./gradlew run again.";

    private final GenericContainer<?> redis = new GenericContainer<>(REDIS_IMAGE).withExposedPorts(6379);
    private final PostgreSQLContainer postgres = new PostgreSQLContainer(POSTGRES_IMAGE);

    public static boolean containerRuntimeAvailable() {
        try {
            return DockerClientFactory.instance().isDockerAvailable();
        } catch (Throwable t) {
            return false;
        }
    }

    public void start() {
        redis.start();
        postgres.start();
    }

    /** A new Redis connection; a short timeout so an unreachable Redis fails fast. */
    public Jedis redis() {
        return new Jedis(new HostAndPort(redis.getHost(), redis.getMappedPort(6379)),
                DefaultJedisClientConfig.builder().timeoutMillis(500).build());
    }

    public Connection database() throws Exception {
        return DriverManager.getConnection(postgres.getJdbcUrl(), postgres.getUsername(), postgres.getPassword());
    }

    /** Freezes the Redis container, as a network cut or a stalled server would. */
    public void pauseRedis() {
        DockerClientFactory.instance().client().pauseContainerCmd(redis.getContainerId()).exec();
    }

    public void unpauseRedis() {
        DockerClientFactory.instance().client().unpauseContainerCmd(redis.getContainerId()).exec();
    }

    @Override
    public void close() {
        redis.stop();
        postgres.stop();
    }
}
