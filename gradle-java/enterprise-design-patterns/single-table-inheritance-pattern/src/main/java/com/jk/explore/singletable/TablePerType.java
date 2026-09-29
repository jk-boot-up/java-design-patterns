package com.jk.explore.singletable;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

/**
 * Without the pattern: one table per product type, so a question about all products asks every table.
 */
public final class TablePerType {

    private int queries;

    public static void create(Connection c) throws SQLException {
        try (Statement s = c.createStatement()) {
            s.execute("CREATE TABLE book (sku VARCHAR(20), name VARCHAR(50), price_pence INT, isbn VARCHAR(20))");
            s.execute("CREATE TABLE food (sku VARCHAR(20), name VARCHAR(50), price_pence INT, best_before VARCHAR(10))");
            s.execute("CREATE TABLE electronics (sku VARCHAR(20), name VARCHAR(50), price_pence INT, warranty_years INT)");
            s.execute("INSERT INTO book VALUES ('BOOK-1', 'Java Basics', 2000, '978-1-00')");
            s.execute("INSERT INTO food VALUES ('TEA-1', 'breakfast tea', 400, '2027-03-01')");
            s.execute("INSERT INTO electronics VALUES ('KETTLE-1', 'steel kettle', 3000, 2)");
            s.execute("INSERT INTO electronics VALUES ('LAMP-1', 'desk lamp', 900, 1)");
        }
    }

    /** "Everything under a price" has to ask all three tables. */
    public List<String> namesUnder(Connection c, int pence) throws SQLException {
        List<String> names = new ArrayList<>();
        for (String table : new String[] {"book", "food", "electronics"}) {
            queries++;
            try (Statement s = c.createStatement();
                 ResultSet rs = s.executeQuery("SELECT name FROM " + table + " WHERE price_pence < " + pence)) {
                while (rs.next()) {
                    names.add(rs.getString(1));
                }
            }
        }
        return names;
    }

    public int queries() {
        return queries;
    }
}
