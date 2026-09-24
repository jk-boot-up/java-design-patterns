package com.jk.explore.idempotentconsumerkafka;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import org.testcontainers.postgresql.PostgreSQLContainer;
import org.testcontainers.utility.DockerImageName;

/**
 * The notifications service's own Postgres database, running in a container that this demo
 * starts and stops itself.
 *
 * <p>It holds two tables. {@code confirmations} is the work: one row for every confirmation
 * email queued for sending. {@code handled_messages} is the pattern: one row for every
 * message the service has finished with, keyed by the message's id. The key is a primary
 * key, so the database itself refuses a second row with the same id; that refusal, not a
 * check in Java, is what stops a duplicate.
 */
public class Database implements AutoCloseable {

    /** Postgres 18.6, the newest release, in its smaller Alpine Linux build. */
    public static final String IMAGE = "postgres:18.6-alpine";

    private final PostgreSQLContainer container =
            new PostgreSQLContainer(DockerImageName.parse(IMAGE).asCompatibleSubstituteFor("postgres"))
                    .withDatabaseName("notifications");

    public void start() {
        container.start();
        run("create table confirmations (id bigserial primary key, order_id text not null, body text not null)");
        run("create table handled_messages (message_id text primary key, order_placed_at timestamptz not null)");
    }

    /** A new connection, as each copy of the service would open its own. */
    public Connection connect() {
        try {
            return DriverManager.getConnection(container.getJdbcUrl(), container.getUsername(), container.getPassword());
        } catch (SQLException e) {
            throw new IllegalStateException("could not connect to Postgres", e);
        }
    }

    /** Clears both tables, so each act starts from nothing. */
    public void empty() {
        run("truncate confirmations, handled_messages");
    }

    public int confirmations() {
        return count("select count(*) from confirmations");
    }

    public int confirmationsFor(String orderId) {
        return count("select count(*) from confirmations where order_id = '" + orderId + "'");
    }

    public int handledIds() {
        return count("select count(*) from handled_messages");
    }

    /** How many database sessions are right now stopped, waiting for another session's lock. */
    public int waitingOnALock() {
        return count("select count(*) from pg_stat_activity where wait_event_type = 'Lock'");
    }

    /** The cleanup job: deletes the ids of every order placed more than this many hours ago. */
    public int forgetIdsOlderThanHours(int hours) {
        try (Connection c = connect(); Statement s = c.createStatement()) {
            return s.executeUpdate("delete from handled_messages where order_placed_at < now() - interval '" + hours + " hours'");
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }

    private int count(String sql) {
        try (Connection c = connect(); Statement s = c.createStatement(); ResultSet r = s.executeQuery(sql)) {
            r.next();
            return r.getInt(1);
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }

    private void run(String sql) {
        try (Connection c = connect(); Statement s = c.createStatement()) {
            s.execute(sql);
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }

    @Override
    public void close() {
        container.stop();
    }
}
