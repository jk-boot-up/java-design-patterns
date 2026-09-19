package com.jk.explore.templatespring;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

/**
 * The same query written twice: once with plain JDBC, where every caller owns the fixed
 * steps, and once with {@link JdbcTemplate}, where the framework owns them and the caller
 * supplies only the part that differs.
 */
@Repository
public class OrderRepository {

    private final DataSource dataSource;
    private final JdbcTemplate jdbc;

    public OrderRepository(DataSource dataSource, JdbcTemplate jdbc) {
        this.dataSource = dataSource;
        this.jdbc = jdbc;
    }

    /** Plain JDBC, the way it was written before templates. It does not close on the error path. */
    public List<String> orderNumbersByHand(String sql) throws SQLException {
        Connection connection = dataSource.getConnection();
        PreparedStatement statement = connection.prepareStatement(sql);
        ResultSet rows = statement.executeQuery();
        List<String> numbers = new ArrayList<>();
        while (rows.next()) {
            numbers.add(rows.getString(1));
        }
        rows.close();
        statement.close();
        connection.close();
        return numbers;
    }

    /** The same query. The only line that is ours is the lambda. */
    public List<String> orderNumbers(String sql) {
        return jdbc.query(sql, (rows, rowNumber) -> rows.getString(1));
    }

    public List<Order> ordersOf(String customer) {
        return jdbc.query("SELECT order_number, customer, total_pence FROM orders WHERE customer = ? ORDER BY order_number",
                (rows, n) -> new Order(rows.getString("order_number"), rows.getString("customer"), rows.getLong("total_pence")),
                customer);
    }

    public Order find(String orderNumber) {
        return jdbc.queryForObject("SELECT order_number, customer, total_pence FROM orders WHERE order_number = ?",
                (rows, n) -> new Order(rows.getString("order_number"), rows.getString("customer"), rows.getLong("total_pence")),
                orderNumber);
    }

    public Order findByCustomerExpectingOne(String customer) {
        return jdbc.queryForObject("SELECT order_number, customer, total_pence FROM orders WHERE customer = ?",
                (rows, n) -> new Order(rows.getString("order_number"), rows.getString("customer"), rows.getLong("total_pence")),
                customer);
    }

    public void insert(String orderNumber, String customer, long totalPence) {
        jdbc.update("INSERT INTO orders VALUES (?, ?, ?)", orderNumber, customer, totalPence);
    }

    public int count() {
        Integer n = jdbc.queryForObject("SELECT COUNT(*) FROM orders", Integer.class);
        return n == null ? 0 : n;
    }

    public int onHand(String sku) {
        Integer n = jdbc.queryForObject("SELECT on_hand FROM stock WHERE sku = ?", Integer.class, sku);
        return n == null ? 0 : n;
    }

    public void reserve(String sku, int quantity) {
        jdbc.update("UPDATE stock SET on_hand = on_hand - ? WHERE sku = ?", quantity, sku);
    }
}
