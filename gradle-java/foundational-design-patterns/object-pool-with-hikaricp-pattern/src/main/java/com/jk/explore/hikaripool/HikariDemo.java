package com.jk.explore.hikaripool;

import com.zaxxer.hikari.HikariDataSource;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.SQLTransientConnectionException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

/** Six acts. Every count comes from HikariCP's own pool statistics. */
public final class HikariDemo {

    public static void main(String[] args) throws Exception {
        System.out.println("OBJECT POOL WITH HIKARICP — the mature answer\n");
        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    private static void actOne() {
        System.out.println("ONE. The pool from the partner project, done by people who did it for years.");
        try (HikariDataSource ds = Payments.pool(2, 1_000)) {
            for (int i = 0; i < 10; i++) {
                Payments.pay(ds, "customer " + i, 1_000);
            }
            System.out.println("  10 payments, " + Payments.count(ds) + " rows written, through a pool that may hold at most 2.");
            System.out.println("  connections HikariCP actually opened: " + ds.getHikariPoolMXBean().getTotalConnections()
                    + ", active " + ds.getHikariPoolMXBean().getActiveConnections() + ", idle " + ds.getHikariPoolMXBean().getIdleConnections()
                    + ". the payments ran one at a time, so one was enough: it opens what demand needs, up to the maximum.");
            System.out.println("  try-with-resources returns each connection: close() on a pooled connection gives it back.\n");
        }
    }

    private static void actTwo() throws SQLException {
        System.out.println("TWO. The dirty return, which the partner project had to fix by hand.");
        try (HikariDataSource ds = Payments.pool(1, 1_000)) {
            try (Connection first = ds.getConnection()) {
                first.setAutoCommit(false);
                first.setReadOnly(true);
                System.out.println("  Ada's borrower sets autoCommit false and readOnly true, then returns the connection.");
            }
            try (Connection second = ds.getConnection()) {
                System.out.println("  Grace's borrower gets the same physical connection: autoCommit " + second.getAutoCommit()
                        + ", readOnly " + second.isReadOnly() + ".");
                System.out.println("  HikariCP reset the JDBC state it knows about on return. that is the reset the partner had to write.");
            }
            try (Connection a = ds.getConnection(); Statement s = a.createStatement()) {
                s.execute("set @card_holder = 'Ada Lovelace'");
            }
            try (Connection b = ds.getConnection(); Statement s = b.createStatement(); ResultSet rs = s.executeQuery("select @card_holder")) {
                rs.next();
                System.out.println("  but state it does not know about stays: a session variable Ada set is read by Grace: " + rs.getString(1));
                System.out.println("  the security bug is still possible. the pool cannot reset what it cannot see.\n");
            }
        }
    }

    private static void actThree() {
        System.out.println("THREE. Exhaustion, with a timeout already built in.");
        try (HikariDataSource ds = Payments.pool(2, 300)) {
            List<Connection> leaked = new ArrayList<>();
            try {
                leaked.add(ds.getConnection());
                leaked.add(ds.getConnection());
                System.out.println("  two borrowers take both connections and never return them.");
                long start = System.nanoTime();
                try {
                    ds.getConnection();
                } catch (SQLTransientConnectionException e) {
                    long millis = (System.nanoTime() - start) / 1_000_000;
                    System.out.println("  a third caller waited " + millis + "ms and got: " + e.getClass().getSimpleName());
                    System.out.println("  " + e.getMessage().replaceAll("payments - ", ""));
                }
                System.out.println("  the timeout is a setting (connectionTimeout), not something you have to remember to write.");
                System.out.println("  its default is thirty seconds, so set it. leakDetectionThreshold can also log who never returned.\n");
            } catch (SQLException e) {
                throw new IllegalStateException(e);
            } finally {
                leaked.forEach(c -> {
                    try {
                        c.close();
                    } catch (SQLException ignored) {
                        // closing returns it to the pool
                    }
                });
            }
        }
    }

    private static void actFour() throws Exception {
        System.out.println("FOUR. Sizing is still a guess, and still costs in both directions.");
        for (int size : new int[]{1, 4}) {
            try (HikariDataSource ds = Payments.pool(size, 5_000, true)) {
                Payments.awaitFilled(ds, size);
                List<Thread> threads = new ArrayList<>();
                long start = System.nanoTime();
                for (int i = 0; i < 4; i++) {
                    Thread t = new Thread(() -> {
                        try (Connection c = ds.getConnection()) {
                            Thread.sleep(50);
                        } catch (Exception e) {
                            throw new IllegalStateException(e);
                        }
                    });
                    threads.add(t);
                    t.start();
                }
                for (Thread t : threads) {
                    t.join();
                }
                System.out.println("  four payments at once, each needing 50ms on a connection, pool of " + size + ": "
                        + (System.nanoTime() - start) / 1_000_000 + "ms");
            }
        }
        try (HikariDataSource ds = Payments.pool(50, 5_000, true)) {
            Payments.awaitFilled(ds, 50);
            System.out.println("  a pool of 50 opens " + ds.getHikariPoolMXBean().getTotalConnections()
                    + " connections and keeps them idle, for four payments.");
        }
        System.out.println("  HikariCP's own documentation argues for small pools. more is not faster.\n");
    }

    private static void actFive() throws SQLException {
        System.out.println("FIVE. What pooling buys, on real JDBC.");
        String url = "jdbc:h2:mem:" + UUID.randomUUID() + ";DB_CLOSE_DELAY=-1";
        try (Connection keepAlive = DriverManager.getConnection(url)) {
            int rounds = 2_000;
            for (int i = 0; i < 500; i++) {
                DriverManager.getConnection(url).close();
            }
            long start = System.nanoTime();
            for (int i = 0; i < rounds; i++) {
                DriverManager.getConnection(url).close();
            }
            long opened = (System.nanoTime() - start) / rounds;
            try (HikariDataSource ds = new HikariDataSource()) {
                ds.setJdbcUrl(url);
                ds.setMaximumPoolSize(2);
                for (int i = 0; i < 500; i++) {
                    ds.getConnection().close();
                }
                start = System.nanoTime();
                for (int i = 0; i < rounds; i++) {
                    ds.getConnection().close();
                }
                long borrowed = (System.nanoTime() - start) / rounds;
                System.out.println(String.format("  opening a new connection each time: about %.1f microseconds.", opened / 1_000.0));
                System.out.println(String.format("  borrowing from the pool:            about %.1f microseconds.", borrowed / 1_000.0));
                System.out.println("  this is an in-memory H2, whose connections are cheap. a real database over a network costs far more,");
                System.out.println("  which is exactly why the pattern is right here. timings vary by machine.\n");
            }
        }
    }

    private static void actSix() {
        System.out.println("SIX. The verdict.");
        System.out.println("  pool connections, threads and native handles, and use a library that has already fixed the hard parts.");
        System.out.println("  never pool ordinary objects, and never write your own connection pool.");
        System.out.println("  where you have met this: every DataSource. Spring Boot's default is HikariCP.");
    }
}
