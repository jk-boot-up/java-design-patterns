package com.jk.explore.transactionaloutboxdebezium;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import org.testcontainers.postgresql.PostgreSQLContainer;
import org.testcontainers.utility.DockerImageName;

/**
 * The Orders service's own Postgres database, running in a container that this demo starts
 * and stops itself.
 *
 * <p>It holds two tables. {@code orders} is the business data. {@code outbox} is the
 * pattern: one row for every message the service owes the rest of the shop, written in the
 * same transaction as the order it is about.
 *
 * <p>Postgres writes every change to a log before it changes any table, so that it can
 * recover after a crash. Postgres calls it the write-ahead log, or WAL. Started with
 * {@code wal_level=logical}, it writes enough into that log for an outside program to read
 * the changes back as rows. That outside program connects through a replication slot: a
 * bookmark that Postgres keeps for one reader, holding on to every part of the log the
 * reader has not yet confirmed.
 */
public class OrdersDatabase implements AutoCloseable {

    /** Postgres 18.6, the newest release, in its smaller Alpine Linux build. */
    public static final String IMAGE = "postgres:18.6-alpine";

    private final PostgreSQLContainer container =
            new PostgreSQLContainer(DockerImageName.parse(IMAGE).asCompatibleSubstituteFor("postgres"))
                    .withDatabaseName("orders")
                    // Logical decoding has to be switched on when Postgres starts; it cannot be
                    // turned on in a running database. Small buffers keep the container light.
                    .withCommand("postgres", "-c", "fsync=off", "-c", "wal_level=logical",
                            "-c", "max_replication_slots=4", "-c", "max_wal_senders=4",
                            "-c", "shared_buffers=32MB");

    public void start() {
        container.start();
        run("create table orders (order_id text primary key, customer text not null, total_pence bigint not null,"
                + " status text not null)");
        run("create table outbox (id text primary key, aggregatetype text not null, aggregateid text not null,"
                + " type text not null, payload text not null)");
    }

    public String host() {
        return container.getHost();
    }

    public int port() {
        return container.getMappedPort(PostgreSQLContainer.POSTGRESQL_PORT);
    }

    public String user() {
        return container.getUsername();
    }

    public String password() {
        return container.getPassword();
    }

    public String databaseName() {
        return container.getDatabaseName();
    }

    /** A new connection, as each service opens its own. */
    public Connection connect() {
        try {
            return DriverManager.getConnection(container.getJdbcUrl(), container.getUsername(), container.getPassword());
        } catch (SQLException e) {
            throw new IllegalStateException("could not connect to Postgres", e);
        }
    }

    /** Clears both tables, so each act starts from nothing. */
    public void empty() {
        run("truncate orders, outbox");
    }

    public int orders() {
        return count("select count(*) from orders");
    }

    public boolean hasOrder(String orderId) {
        return count("select count(*) from orders where order_id = '" + orderId + "'") == 1;
    }

    public int outboxRows() {
        return count("select count(*) from outbox");
    }

    /** The setting Postgres was started with: logical, replica or minimal. */
    public String walLevel() {
        return text("show wal_level");
    }

    /** How much log Postgres may keep for a slot before giving up on it; -1 means no limit. */
    public String slotLogLimit() {
        return text("show max_slot_wal_keep_size");
    }

    /** True when a reader is connected to the slot right now. */
    public boolean slotActive(String slot) {
        return "t".equals(text("select active from pg_replication_slots where slot_name = '" + slot + "'"));
    }

    public boolean slotExists(String slot) {
        return count("select count(*) from pg_replication_slots where slot_name = '" + slot + "'") == 1;
    }

    /** How many bytes of log Postgres is keeping on disk because the slot's reader has not confirmed them. */
    public long logHeldForSlot(String slot) {
        return Long.parseLong(text("select pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)::bigint"
                + " from pg_replication_slots where slot_name = '" + slot + "'"));
    }

    /** Removes the slot, which is what has to happen when its reader is retired for good. */
    public void dropSlot(String slot) {
        run("select pg_drop_replication_slot('" + slot + "')");
    }

    private String text(String sql) {
        try (Connection c = connect(); Statement s = c.createStatement(); ResultSet r = s.executeQuery(sql)) {
            r.next();
            return r.getString(1);
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }

    private int count(String sql) {
        return Integer.parseInt(text(sql));
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
