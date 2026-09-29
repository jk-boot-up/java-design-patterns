package com.jk.explore.tdgjdbc;

import java.util.ArrayList;
import java.util.List;
import javax.sql.DataSource;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.dao.DataAccessException;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.jdbc.core.JdbcTemplate;

/**
 * The five acts, with Spring's JdbcTemplate and an in-memory H2 database.
 */
public final class JdbcTemplateGatewayDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();
        try (ConfigurableApplicationContext ctx = new SpringApplicationBuilder(ShopApp.class)
                .properties("spring.main.banner-mode=off", "logging.level.root=OFF",
                        "spring.datasource.url=jdbc:h2:mem:shop", "spring.sql.init.mode=always",
                        "spring.datasource.hikari.maximum-pool-size=2", "spring.datasource.hikari.connection-timeout=250")
                .run()) {
            DataSource pool = ctx.getBean(DataSource.class);

            out.add("ONE. Every page writes its own JDBC, and one forgets to close.");
            for (int i = 0; i < 2; i++) {
                try {
                    out.add("  product page: " + ScatteredJdbc.productPage(pool, "KETTLE-1") + " (connection not closed)");
                } catch (Exception e) {
                    out.add("  product page: FAILED, " + e.getClass().getSimpleName());
                }
            }
            try {
                ScatteredJdbc.productPage(pool, "KETTLE-1");
                out.add("  third page: served");
            } catch (Exception e) {
                out.add("  third page: FAILED after 0.25 s, the pool of 2 connections is empty");
            }
        }

        try (ConfigurableApplicationContext ctx = new SpringApplicationBuilder(ShopApp.class)
                .properties("spring.main.banner-mode=off", "logging.level.root=OFF",
                        "spring.datasource.url=jdbc:h2:mem:shop2", "spring.sql.init.mode=always",
                        "spring.datasource.hikari.maximum-pool-size=2", "spring.datasource.hikari.connection-timeout=250")
                .run()) {
            ProductGateway gateway = ctx.getBean(ProductGateway.class);

            out.add("");
            out.add("TWO. A table data gateway on JdbcTemplate: all the product SQL in one class.");
            for (int i = 0; i < 3; i++) {
                gateway.find("KETTLE-1");
            }
            Row kettle = gateway.find("KETTLE-1");
            out.add("  product page, asked 4 times on a pool of 2: " + kettle.name() + ", " + kettle.quantity() + " in stock");
            out.add("  stock report: " + gateway.countOutOfStock() + " product out of stock");
            out.add("  cheaper than £10: " + gateway.cheaperThan(1000).stream().map(Row::name).toList());
            out.add("  JdbcTemplate borrowed and returned every connection; DataClassRowMapper built the Row records");

            out.add("");
            out.add("THREE. Database errors become Spring exceptions, not vendor codes.");
            JdbcTemplate plain = ctx.getBean(JdbcTemplate.class);
            plain.execute("ALTER TABLE product ALTER COLUMN quantity RENAME TO stock");
            try {
                gateway.find("KETTLE-1");
            } catch (DataAccessException e) {
                out.add("  the column is renamed behind the gateway's back: " + e.getClass().getSimpleName());
            }
            plain.execute("ALTER TABLE product ALTER COLUMN stock RENAME TO quantity");
            try {
                gateway.insert(new Row("MUG-1", "another mug", 800, 1));
            } catch (DuplicateKeyException e) {
                out.add("  a second MUG-1: " + e.getClass().getSimpleName() + ", whatever the database brand");
            }

            out.add("");
            out.add("FOUR. Stock taken in one statement.");
            int taken = 0;
            for (int i = 0; i < 4; i++) {
                if (gateway.takeOne("LAMP-1")) {
                    taken++;
                }
            }
            out.add("  4 customers try for 2 desk lamps: " + taken + " taken, stock now " + gateway.find("LAMP-1").quantity()
                    + " (UPDATE ... WHERE quantity > 0)");

            out.add("");
            out.add("FIVE. The bill: rows, not objects with rules.");
            out.add("  a Row is data only: \"low on stock\" must be decided by each caller");
            out.add("  the gateway grows a method for every question, and its SQL is still text, checked only when it runs");
        }
        return out;
    }

    private JdbcTemplateGatewayDemo() {
    }
}
