package com.jk.explore.hikaripool;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.UUID;

/**
 * A payments table over in-memory H2, behind a real HikariCP pool. The partner
 * project, Object Pool, built a pool by hand and found its costs. HikariCP is
 * the mature answer to several of them, and this shows which, and which remain.
 */
public final class Payments {

    private Payments() {
    }

    /** A pool that opens connections only as demand needs them, up to the maximum. Its counts are deterministic. */
    public static HikariDataSource pool(int maximumPoolSize, long connectionTimeoutMillis) {
        return pool(maximumPoolSize, connectionTimeoutMillis, false);
    }

    /** When {@code warm}, HikariCP fills the pool to its maximum in the background, which takes a moment. */
    public static HikariDataSource pool(int maximumPoolSize, long connectionTimeoutMillis, boolean warm) {
        HikariConfig config = new HikariConfig();
        if (!warm) {
            config.setMinimumIdle(0);
        }
        config.setJdbcUrl("jdbc:h2:mem:" + UUID.randomUUID() + ";DB_CLOSE_DELAY=-1");
        config.setMaximumPoolSize(maximumPoolSize);
        config.setConnectionTimeout(connectionTimeoutMillis);
        config.setPoolName("payments");
        HikariDataSource ds = new HikariDataSource(config);
        try (Connection c = ds.getConnection(); Statement s = c.createStatement()) {
            s.execute("create table payment (id identity primary key, card_holder varchar(50), pence bigint)");
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
        return ds;
    }

    /** HikariCP fills its pool in the background. Wait until it is full, so a measurement starts warm. */
    public static void awaitFilled(HikariDataSource ds, int size) {
        long deadline = System.nanoTime() + 5_000_000_000L;
        while (ds.getHikariPoolMXBean().getTotalConnections() < size && System.nanoTime() < deadline) {
            try {
                Thread.sleep(10);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
        }
    }

    public static void pay(HikariDataSource ds, String cardHolder, long pence) {
        try (Connection c = ds.getConnection();
             PreparedStatement p = c.prepareStatement("insert into payment (card_holder, pence) values (?, ?)")) {
            p.setString(1, cardHolder);
            p.setLong(2, pence);
            p.executeUpdate();
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }

    public static long count(HikariDataSource ds) {
        try (Connection c = ds.getConnection(); Statement s = c.createStatement();
             var rs = s.executeQuery("select count(*) from payment")) {
            rs.next();
            return rs.getLong(1);
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }
}
