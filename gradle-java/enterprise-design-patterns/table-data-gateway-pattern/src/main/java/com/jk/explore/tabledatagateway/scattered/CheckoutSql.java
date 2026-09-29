package com.jk.explore.tabledatagateway.scattered;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

/**
 * Without the pattern: checkout updates stock with its own SQL.
 */
public final class CheckoutSql {

    public static void take(Connection c, String sku, int qty) throws SQLException {
        try (PreparedStatement ps = c.prepareStatement("UPDATE product SET stock = stock - ? WHERE sku = ?")) {
            ps.setInt(1, qty);
            ps.setString(2, sku);
            ps.executeUpdate();
        }
    }

    private CheckoutSql() {
    }
}
