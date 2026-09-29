package com.jk.explore.shardingpostgres;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.IntStream;
import org.testcontainers.DockerClientFactory;
import org.testcontainers.postgresql.PostgreSQLContainer;

/**
 * Real PostgreSQL databases, one container each, started and stopped by this demo.
 */
public final class Shards implements AutoCloseable {

    public static final String IMAGE = "postgres:18.6-alpine";

    public static final String NO_RUNTIME_ADVICE =
            "This demo needs a container runtime, because it starts real PostgreSQL databases.\n"
            + "Start Docker Desktop, or any Docker-compatible runtime, wait until it says it is running, and run ./gradlew run again.";

    public static final String WOULD_NOT_START_ADVICE =
            "The PostgreSQL containers would not start. The image is " + IMAGE + ".\n"
            + "Check that the container runtime is running and can reach the internet, then run ./gradlew run again.";

    private final List<PostgreSQLContainer> databases = new ArrayList<>();

    public Shards(int count) {
        for (int i = 0; i < count; i++) {
            databases.add(new PostgreSQLContainer(IMAGE));
        }
    }

    public static boolean containerRuntimeAvailable() {
        try {
            return DockerClientFactory.instance().isDockerAvailable();
        } catch (Throwable t) {
            return false;
        }
    }

    /** Starts every database at once, then creates the same tables on each. */
    public void start() throws Exception {
        IntStream.range(0, databases.size()).parallel().forEach(i -> databases.get(i).start());
        for (int i = 0; i < databases.size(); i++) {
            try (Connection c = connect(i); Statement s = c.createStatement()) {
                s.execute("CREATE TABLE orders (id TEXT PRIMARY KEY, customer INT NOT NULL, pence INT NOT NULL)");
                s.execute("CREATE TABLE redemptions (coupon TEXT UNIQUE, customer INT NOT NULL)");
            }
        }
    }

    public int size() {
        return databases.size();
    }

    public Connection connect(int i) throws Exception {
        PostgreSQLContainer d = databases.get(i);
        return DriverManager.getConnection(d.getJdbcUrl(), d.getUsername(), d.getPassword());
    }

    @Override
    public void close() {
        databases.forEach(PostgreSQLContainer::stop);
    }
}
