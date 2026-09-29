package com.jk.explore.tabledatagateway.scattered;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * Without the pattern: the stock report writes its own SQL too.
 */
public final class StockReport {

    public static int outOfStock(Connection c) throws SQLException {
        try (Statement s = c.createStatement();
             ResultSet rs = s.executeQuery("SELECT COUNT(*) FROM product WHERE stock = 0")) {
            rs.next();
            return rs.getInt(1);
        }
    }

    private StockReport() {
    }
}
