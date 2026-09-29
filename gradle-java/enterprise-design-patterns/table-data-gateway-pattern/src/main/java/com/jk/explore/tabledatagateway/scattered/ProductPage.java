package com.jk.explore.tabledatagateway.scattered;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * Without the pattern: the product page writes its own SQL.
 */
public final class ProductPage {

    public static String show(Connection c, String sku) throws SQLException {
        try (PreparedStatement ps = c.prepareStatement("SELECT name, price_pence, stock FROM product WHERE sku = ?")) {
            ps.setString(1, sku);
            try (ResultSet rs = ps.executeQuery()) {
                rs.next();
                return rs.getString("name") + ", " + rs.getInt("stock") + " in stock";
            }
        }
    }

    private ProductPage() {
    }
}
