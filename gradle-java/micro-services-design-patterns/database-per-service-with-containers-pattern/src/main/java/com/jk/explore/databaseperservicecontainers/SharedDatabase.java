package com.jk.explore.databaseperservicecontainers;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

/**
 * Before the split: one Postgres database, {@code shop}, holding both teams' tables.
 *
 * <p>The Catalog team owns {@code products}. The Orders team owns {@code orders}. A
 * foreign key — a rule the database itself keeps — says every order's sku must be a
 * product that exists. The order history page is one SQL query that joins the two tables,
 * and it names the Catalog team's column {@code product_name} directly.
 */
public class SharedDatabase implements AutoCloseable {

    public static final String NAME = "shop";

    /** The Orders team's query. It reaches into the Catalog team's table by column name. */
    static final String ORDER_HISTORY_JOIN =
            "SELECT o.order_id, o.sku, p.product_name, o.quantity"
            + " FROM orders o JOIN products p ON p.sku = o.sku"
            + " WHERE o.customer_id = ? ORDER BY o.order_id";

    private final Connection connection;
    private final RoundTrips roundTrips = new RoundTrips();

    public SharedDatabase(Postgres postgres) {
        postgres.createDatabase(NAME);
        this.connection = postgres.connectTo(NAME);
        run("CREATE TABLE products (sku TEXT PRIMARY KEY, product_name TEXT NOT NULL)");
        run("CREATE TABLE orders (order_id TEXT PRIMARY KEY, customer_id TEXT NOT NULL,"
                + " sku TEXT NOT NULL REFERENCES products (sku), quantity INT NOT NULL)");
    }

    public void addProduct(String sku, String name) {
        update("INSERT INTO products (sku, product_name) VALUES (?, ?)", sku, name);
    }

    public void addOrder(Order order) {
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

    /** The order history page: one query, one join, done by Postgres. */
    public List<OrderHistoryRow> orderHistory(String customerId) throws SQLException {
        roundTrips.one();
        List<OrderHistoryRow> rows = new ArrayList<>();
        try (PreparedStatement s = connection.prepareStatement(ORDER_HISTORY_JOIN)) {
            s.setString(1, customerId);
            try (ResultSet r = s.executeQuery()) {
                while (r.next()) {
                    rows.add(new OrderHistoryRow(r.getString(1), r.getString(2), r.getString(3), r.getInt(4)));
                }
            }
        }
        return rows;
    }

    /** The Catalog team deletes a product. Postgres checks the foreign key first. */
    public void deleteProduct(String sku) throws SQLException {
        try (PreparedStatement s = connection.prepareStatement("DELETE FROM products WHERE sku = ?")) {
            s.setString(1, sku);
            s.executeUpdate();
        }
    }

    /** The Catalog team's migration: a correct change to a table they own. */
    public void renameProductNameColumnTo(String newName) {
        run("ALTER TABLE products RENAME COLUMN product_name TO " + newName);
    }

    public int roundTrips() {
        return roundTrips.count();
    }

    private void run(String sql) {
        try (Statement s = connection.createStatement()) {
            s.execute(sql);
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }

    private void update(String sql, String a, String b) {
        try (PreparedStatement s = connection.prepareStatement(sql)) {
            s.setString(1, a);
            s.setString(2, b);
            s.executeUpdate();
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }

    @Override
    public void close() {
        try {
            connection.close();
        } catch (SQLException ignored) {
            // closing is best effort; the container is removed at the end anyway
        }
    }
}
