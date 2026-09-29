package com.jk.explore.tabledatagateway;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * A fresh in-memory H2 database with the shop's product table and four products.
 */
public final class Database {

    public static Connection open(String name) throws SQLException {
        Connection c = DriverManager.getConnection("jdbc:h2:mem:" + name);
        try (Statement s = c.createStatement()) {
            s.execute("CREATE TABLE product (sku VARCHAR(20) PRIMARY KEY, name VARCHAR(50),"
                    + " price_pence INT, stock INT)");
            s.execute("INSERT INTO product VALUES ('KETTLE-1', 'steel kettle', 3000, 4),"
                    + " ('TEAPOT-1', 'glass teapot', 2500, 0), ('MUG-1', 'mug', 800, 20),"
                    + " ('TOWEL-1', 'tea towel', 600, 12)");
        }
        return c;
    }

    /** The database team renames a column, as happens to every real schema eventually. */
    public static void renameStockColumn(Connection c) throws SQLException {
        try (Statement s = c.createStatement()) {
            s.execute("ALTER TABLE product RENAME COLUMN stock TO quantity");
        }
    }

    private Database() {
    }
}
