package com.jk.explore.singletable;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: a table per type, one table for all, each row becoming its own class, a new type, and the bill.
 */
public final class SingleTableDemo {

    public static void main(String[] args) throws SQLException {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    static Connection open(String name) throws SQLException {
        return DriverManager.getConnection("jdbc:h2:mem:" + name);
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws SQLException {
        List<String> out = new ArrayList<>();

        out.add("ONE. A table for every product type.");
        try (Connection c = open("per-type")) {
            TablePerType.create(c);
            TablePerType t = new TablePerType();
            out.add("  everything under £10: " + t.namesUnder(c, 1000) + ", " + t.queries() + " queries, one per table");
            out.add("  a fourth type means a fourth table, and every such question grows again");
        }

        out.add("");
        out.add("TWO. Single table inheritance: every type in one table, with a type column.");
        try (Connection c = open("single")) {
            ProductTable table = new ProductTable(c);
            table.create();
            List<Products.Product> cheap = table.under(1000);
            out.add("  everything under £10: " + cheap.stream().map(Products.Product::name).toList()
                    + ", " + table.queries() + " query");

            out.add("");
            out.add("THREE. Each row comes back as its own class.");
            for (Products.Product p : table.all()) {
                out.add("  " + p.sku() + " -> " + p.getClass().getSimpleName() + ": " + p.packingNote());
            }

            out.add("");
            out.add("FOUR. A new type: one class and one new column.");
            table.addGiftCards();
            table.insert(new Products.GiftCard("GIFT-1", "gift card", 5000, 5000));
            out.add("  ALTER TABLE product ADD COLUMN value_pence; existing rows untouched");
            out.add("  GIFT-1 -> " + table.all().get(1).getClass().getSimpleName() + ": " + table.all().get(1).packingNote());

            out.add("");
            out.add("FIVE. The bill: empty cells, and rules the database cannot keep.");
            int[] empty = table.emptyCells();
            out.add("  " + empty[0] + " of " + empty[1] + " type-specific cells are empty (NULL)");
            table.insert(new Products.Book("BOOK-2", "no-ISBN book", 1500, null));
            out.add("  a book without an ISBN was saved: the column cannot be NOT NULL,"
                    + " because food and kettles leave it empty");
        }
        return out;
    }

    private SingleTableDemo() {
    }
}
