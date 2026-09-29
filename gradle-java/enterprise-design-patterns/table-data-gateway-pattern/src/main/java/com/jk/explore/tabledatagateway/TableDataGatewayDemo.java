package com.jk.explore.tabledatagateway;

import com.jk.explore.tabledatagateway.scattered.CheckoutSql;
import com.jk.explore.tabledatagateway.scattered.ProductPage;
import com.jk.explore.tabledatagateway.scattered.StockReport;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

/**
 * The five acts: SQL in every caller, a table data gateway, a renamed column, where the SQL lives, and the bill.
 */
public final class TableDataGatewayDemo {

    static final Path SOURCES = Path.of("src/main/java/com/jk/explore/tabledatagateway");

    public static void main(String[] args) throws SQLException {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws SQLException {
        List<String> out = new ArrayList<>();

        out.add("ONE. Every caller writes its own SQL.");
        try (Connection c = Database.open("scattered")) {
            out.add("  product page: " + ProductPage.show(c, "KETTLE-1"));
            out.add("  stock report: " + StockReport.outOfStock(c) + " product out of stock");
            CheckoutSql.take(c, "KETTLE-1", 1);
            out.add("  checkout took 1 kettle: " + ProductPage.show(c, "KETTLE-1"));
            Database.renameStockColumn(c);
            out.add("  the database team renames stock to quantity...");
            out.add("  product page: " + attempt(() -> ProductPage.show(c, "KETTLE-1")));
            out.add("  stock report: " + attempt(() -> String.valueOf(StockReport.outOfStock(c))));
            out.add("  checkout:     " + attempt(() -> {
                CheckoutSql.take(c, "KETTLE-1", 1);
                return "ok";
            }));
        }

        out.add("");
        out.add("TWO. A table data gateway: all the product table's SQL in one class.");
        try (Connection c = Database.open("gateway")) {
            ProductGateway g = new ProductGateway(c);
            out.add("  product page: " + Pages.productPage(g, "KETTLE-1"));
            out.add("  stock report: " + Pages.stockReport(g) + " product out of stock");
            Pages.checkout(g, "KETTLE-1", 1);
            out.add("  checkout took 1 kettle: " + Pages.productPage(g, "KETTLE-1"));
            out.add("  cheaper than £10: " + g.cheaperThan(1000).stream().map(ProductGateway.Row::name).toList());

            out.add("");
            out.add("THREE. The same rename, fixed in one place.");
            Database.renameStockColumn(c);
            ProductGateway fixed = new ProductGateway(c, "quantity");
            out.add("  gateway told the column's new name, once");
            out.add("  product page: " + Pages.productPage(fixed, "KETTLE-1"));
            out.add("  stock report: " + Pages.stockReport(fixed) + " product out of stock");
            Pages.checkout(fixed, "KETTLE-1", 1);
            out.add("  checkout took 1 kettle: " + Pages.productPage(fixed, "KETTLE-1"));
        }

        out.add("");
        out.add("FOUR. Where the SQL lives now.");
        out.add("  classes that mention the product table, old way: " + count("scattered", "FROM product", "UPDATE product"));
        out.add("  callers that mention it, new way: " + countFile("Pages.java", "product ") + "; the gateway: 1 class");
        out.add("  callers get plain Row records: no connections, no result sets, no SQL");

        out.add("");
        out.add("FIVE. The bill: rows, not objects with rules.");
        out.add("  a Row is data only: \"low on stock\" must be decided by each caller");
        out.add("  and the gateway grows a method for every question anyone asks the table");
        return out;
    }

    interface Attempt {
        String run() throws SQLException;
    }

    static String attempt(Attempt a) {
        try {
            return a.run();
        } catch (SQLException e) {
            return "FAILED, " + e.getMessage().split(";")[0];
        }
    }

    static long count(String folder, String... needles) {
        try (Stream<Path> files = Files.list(SOURCES.resolve(folder))) {
            return files.filter(f -> {
                try {
                    String s = Files.readString(f);
                    return Stream.of(needles).anyMatch(s::contains);
                } catch (IOException e) {
                    throw new UncheckedIOException(e);
                }
            }).count();
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    static int countFile(String file, String needle) {
        try {
            return Files.readString(SOURCES.resolve(file)).contains("FROM " + needle.trim()) ? 1 : 0;
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    private TableDataGatewayDemo() {
    }
}
