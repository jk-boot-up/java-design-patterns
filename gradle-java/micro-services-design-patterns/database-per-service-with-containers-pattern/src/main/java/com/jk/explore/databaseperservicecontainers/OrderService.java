package com.jk.explore.databaseperservicecontainers;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

/**
 * The Orders service. It owns the {@code orders} database on Postgres, and it holds a
 * connection to that database and to nothing else.
 *
 * <p>That last sentence is the whole pattern. The Orders service has no MongoDB client,
 * no MongoDB address and no MongoDB password. There is no query it could write that
 * reaches the Catalog's products.
 */
public class OrderService implements AutoCloseable {

    private final Connection connection;
    private final RoundTrips roundTrips;

    public OrderService(Postgres postgres, RoundTrips roundTrips) {
        this.connection = postgres.connectTo(Postgres.ORDERS_DATABASE);
        this.roundTrips = roundTrips;
        try (Statement s = connection.createStatement()) {
            s.execute("DROP TABLE IF EXISTS orders");
            s.execute("CREATE TABLE orders (order_id TEXT PRIMARY KEY, customer_id TEXT NOT NULL,"
                    + " sku TEXT NOT NULL, quantity INT NOT NULL CHECK (quantity > 0))");
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }

    public void insert(Order order) {
        try (PreparedStatement s = connection.prepareStatement(
                "INSERT INTO orders (order_id, customer_id, sku, quantity) VALUES (?, ?, ?, ?)")) {
            s.setString(1, order.orderId());
            s.setString(2, order.customerId());
            s.setString(3, order.sku());
            s.setInt(4, order.quantity());
            s.executeUpdate();
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }

    /** One customer's orders, in one SQL query. No product names: those are not Orders' data. */
    public List<Order> ordersFor(String customerId) {
        roundTrips.one();
        List<Order> orders = new ArrayList<>();
        try (PreparedStatement s = connection.prepareStatement(
                "SELECT order_id, customer_id, sku, quantity FROM orders WHERE customer_id = ? ORDER BY order_id")) {
            s.setString(1, customerId);
            try (ResultSet r = s.executeQuery()) {
                while (r.next()) {
                    orders.add(new Order(r.getString(1), r.getString(2), r.getString(3), r.getInt(4)));
                }
            }
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
        return orders;
    }

    /** How many tables the Orders database holds. One: its own. */
    public int tables() {
        return count("SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public'");
    }

    /** How many orders name this sku. Asked only of Orders' own table. */
    public int ordersNaming(String sku) {
        try (PreparedStatement s = connection.prepareStatement("SELECT count(*) FROM orders WHERE sku = ?")) {
            s.setString(1, sku);
            try (ResultSet r = s.executeQuery()) {
                r.next();
                return r.getInt(1);
            }
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }

    /**
     * Runs a query exactly as written and returns Postgres's refusal, or null if it ran.
     * Used to try the old join against a database that no longer holds the other half.
     */
    public String tryToRun(String sql) {
        try (Statement s = connection.createStatement()) {
            s.executeQuery(sql).close();
            return null;
        } catch (SQLException e) {
            return SqlError.describe(e);
        }
    }

    /** Starts a transaction: nothing written from here is kept until {@link #commit()}. */
    public void begin() {
        try {
            connection.setAutoCommit(false);
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }

    public void commit() {
        try {
            connection.commit();
            connection.setAutoCommit(true);
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }

    /** Undoes everything written since {@link #begin()} — in Postgres, and only in Postgres. */
    public void rollback() {
        try {
            connection.rollback();
            connection.setAutoCommit(true);
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }

    private int count(String sql) {
        try (Statement s = connection.createStatement(); ResultSet r = s.executeQuery(sql)) {
            r.next();
            return r.getInt(1);
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }

    @Override
    public void close() {
        try {
            connection.close();
        } catch (SQLException ignored) {
            // best effort
        }
    }
}
