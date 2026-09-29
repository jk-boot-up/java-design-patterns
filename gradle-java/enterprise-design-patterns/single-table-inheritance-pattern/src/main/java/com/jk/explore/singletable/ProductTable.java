package com.jk.explore.singletable;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

/**
 * The pattern: every product type in one table, with a type column saying which class each row becomes.
 *
 * <p>Columns that belong to only one type (isbn, best_before, ...) are
 * empty (NULL) for the others. Loading reads the type column and builds the
 * matching class.
 */
public final class ProductTable {

    private final Connection c;
    private int queries;

    public ProductTable(Connection c) {
        this.c = c;
    }

    public void create() throws SQLException {
        try (Statement s = c.createStatement()) {
            s.execute("CREATE TABLE product (sku VARCHAR(20) PRIMARY KEY, type VARCHAR(12) NOT NULL,"
                    + " name VARCHAR(50), price_pence INT,"
                    + " isbn VARCHAR(20), best_before VARCHAR(10), warranty_years INT)");
        }
        insert(new Products.Book("BOOK-1", "Java Basics", 2000, "978-1-00"));
        insert(new Products.Food("TEA-1", "breakfast tea", 400, "2027-03-01"));
        insert(new Products.Electronics("KETTLE-1", "steel kettle", 3000, 2));
        insert(new Products.Electronics("LAMP-1", "desk lamp", 900, 1));
    }

    /** Act four: a new type needs one new, empty-for-everyone-else column. */
    public void addGiftCards() throws SQLException {
        try (Statement s = c.createStatement()) {
            s.execute("ALTER TABLE product ADD COLUMN value_pence INT");
        }
    }

    public void insert(Products.Product p) throws SQLException {
        String sql = p instanceof Products.GiftCard
                ? "INSERT INTO product (sku, type, name, price_pence, value_pence) VALUES (?, ?, ?, ?, ?)"
                : "INSERT INTO product (sku, type, name, price_pence, isbn, best_before, warranty_years) VALUES (?, ?, ?, ?, ?, ?, ?)";
        try (PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, p.sku());
            ps.setString(2, p.getClass().getSimpleName().toUpperCase());
            ps.setString(3, p.name());
            ps.setInt(4, p.pricePence());
            switch (p) {
                case Products.Book b -> { ps.setString(5, b.isbn()); ps.setString(6, null); ps.setObject(7, null); }
                case Products.Food f -> { ps.setString(5, null); ps.setString(6, f.bestBefore()); ps.setObject(7, null); }
                case Products.Electronics e -> { ps.setString(5, null); ps.setString(6, null); ps.setObject(7, e.warrantyYears()); }
                case Products.GiftCard g -> ps.setObject(5, g.valuePence());
            }
            ps.executeUpdate();
        }
    }

    public List<Products.Product> under(int pence) throws SQLException {
        return load("SELECT * FROM product WHERE price_pence < " + pence + " ORDER BY price_pence");
    }

    public List<Products.Product> all() throws SQLException {
        return load("SELECT * FROM product ORDER BY sku");
    }

    /** How many of the four type-specific cells are empty, once gift cards exist: the space the pattern wastes. */
    public int[] emptyCells() throws SQLException {
        try (Statement s = c.createStatement();
             ResultSet rs = s.executeQuery("SELECT COUNT(*),"
                     + " SUM(CASE WHEN isbn IS NULL THEN 1 ELSE 0 END) + SUM(CASE WHEN best_before IS NULL THEN 1 ELSE 0 END)"
                     + " + SUM(CASE WHEN warranty_years IS NULL THEN 1 ELSE 0 END)"
                     + " + SUM(CASE WHEN value_pence IS NULL THEN 1 ELSE 0 END) FROM product")) {
            rs.next();
            return new int[] {rs.getInt(2), rs.getInt(1) * 4};
        }
    }

    private List<Products.Product> load(String sql) throws SQLException {
        queries++;
        List<Products.Product> out = new ArrayList<>();
        try (Statement s = c.createStatement(); ResultSet rs = s.executeQuery(sql)) {
            boolean hasValue = rs.getMetaData().getColumnCount() > 7;
            while (rs.next()) {
                String sku = rs.getString("sku");
                String name = rs.getString("name");
                int price = rs.getInt("price_pence");
                out.add(switch (rs.getString("type")) {
                    case "BOOK" -> new Products.Book(sku, name, price, rs.getString("isbn"));
                    case "FOOD" -> new Products.Food(sku, name, price, rs.getString("best_before"));
                    case "ELECTRONICS" -> new Products.Electronics(sku, name, price, (Integer) rs.getObject("warranty_years"));
                    case "GIFTCARD" -> new Products.GiftCard(sku, name, price, hasValue ? (Integer) rs.getObject("value_pence") : null);
                    default -> throw new IllegalStateException("unknown type " + rs.getString("type"));
                });
            }
        }
        return out;
    }

    public int queries() {
        return queries;
    }
}
