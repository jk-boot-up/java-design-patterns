package com.jk.explore.tabledatagateway;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * The pattern: the one class that holds every piece of SQL for the product table.
 *
 * <p>Callers ask it plain questions (find by code, list what is cheaper than
 * a price, take stock) and get plain records back. They never see SQL,
 * connections or result sets. The stock column's name is written here, once.
 */
public final class ProductGateway {

    /** One row of the product table. */
    public record Row(String sku, String name, int pricePence, int stock) {
    }

    private final Connection c;
    private final String stock;

    public ProductGateway(Connection c) {
        this(c, "stock");
    }

    /** The column's name is kept in exactly one place: here. */
    public ProductGateway(Connection c, String stockColumn) {
        this.c = c;
        this.stock = stockColumn;
    }

    public Optional<Row> findBySku(String sku) {
        List<Row> rows = query("SELECT sku, name, price_pence, " + stock + " FROM product WHERE sku = ?", sku);
        return rows.stream().findFirst();
    }

    public List<Row> cheaperThan(int pence) {
        return query("SELECT sku, name, price_pence, " + stock + " FROM product WHERE price_pence < ? ORDER BY price_pence", pence);
    }

    public int countOutOfStock() {
        return query("SELECT sku, name, price_pence, " + stock + " FROM product WHERE " + stock + " = 0").size();
    }

    public void takeStock(String sku, int qty) {
        try (PreparedStatement ps = c.prepareStatement("UPDATE product SET " + stock + " = " + stock + " - ? WHERE sku = ?")) {
            ps.setInt(1, qty);
            ps.setString(2, sku);
            ps.executeUpdate();
        } catch (SQLException e) {
            throw new IllegalStateException(e.getMessage(), e);
        }
    }

    private List<Row> query(String sql, Object... values) {
        try (PreparedStatement ps = c.prepareStatement(sql)) {
            for (int i = 0; i < values.length; i++) {
                ps.setObject(i + 1, values[i]);
            }
            try (ResultSet rs = ps.executeQuery()) {
                List<Row> rows = new ArrayList<>();
                while (rs.next()) {
                    rows.add(new Row(rs.getString(1), rs.getString(2), rs.getInt(3), rs.getInt(4)));
                }
                return rows;
            }
        } catch (SQLException e) {
            throw new IllegalStateException(e.getMessage(), e);
        }
    }
}
