package com.jk.explore.databaseperservicecontainers;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import org.testcontainers.postgresql.PostgreSQLContainer;
import org.testcontainers.utility.DockerImageName;

/**
 * A real PostgreSQL server, running in a container that this demo starts and stops itself.
 *
 * <p>Postgres is a relational database: data lives in tables with fixed columns, it is
 * asked questions in SQL, and it can join two tables in one query and refuse a change that
 * would break a rule between them. One Postgres server can hold several separate
 * databases. This project uses two of them: {@code shop}, the shared database both teams
 * used before the split, and {@code orders}, the database the Orders service owns after it.
 */
public class Postgres implements AutoCloseable {

    /** PostgreSQL 18.6 on Alpine Linux, the newest release at the time this project was written. */
    public static final String IMAGE = "postgres:18.6-alpine";

    /** The database the container creates for us. The Orders service's own. */
    public static final String ORDERS_DATABASE = "orders";

    private final PostgreSQLContainer container =
            new PostgreSQLContainer(DockerImageName.parse(IMAGE))
                    .withDatabaseName(ORDERS_DATABASE)
                    .withUsername("shop")
                    .withPassword("shop");

    public void start() {
        container.start();
    }

    /** A new connection to one database on this server. The port is a random free one. */
    public Connection connectTo(String database) {
        String url = "jdbc:postgresql://" + container.getHost() + ":"
                + container.getMappedPort(PostgreSQLContainer.POSTGRESQL_PORT) + "/" + database;
        try {
            return DriverManager.getConnection(url, container.getUsername(), container.getPassword());
        } catch (SQLException e) {
            throw new IllegalStateException("could not connect to " + database, e);
        }
    }

    /** Makes a second, separate database on the same server. */
    public void createDatabase(String database) {
        try (Connection c = connectTo(ORDERS_DATABASE); Statement s = c.createStatement()) {
            s.execute("DROP DATABASE IF EXISTS " + database);
            s.execute("CREATE DATABASE " + database);
        } catch (SQLException e) {
            throw new IllegalStateException("could not create " + database, e);
        }
    }

    public void stop() {
        container.stop();
    }

    @Override
    public void close() {
        stop();
    }
}
