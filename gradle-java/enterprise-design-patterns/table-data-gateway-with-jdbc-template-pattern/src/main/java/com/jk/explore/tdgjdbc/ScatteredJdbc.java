package com.jk.explore.tdgjdbc;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import javax.sql.DataSource;

/**
 * Before: a page that writes its own JDBC, and forgets to close the connection it borrowed.
 */
public final class ScatteredJdbc {

    public static String productPage(DataSource pool, String sku) throws Exception {
        Connection c = pool.getConnection();                 // borrowed from the pool ...
        PreparedStatement p = c.prepareStatement("SELECT name, quantity FROM product WHERE sku = ?");
        p.setString(1, sku);
        ResultSet r = p.executeQuery();
        r.next();
        return r.getString(1) + ", " + r.getInt(2) + " in stock";   // ... and never given back
    }

    private ScatteredJdbc() {
    }
}
