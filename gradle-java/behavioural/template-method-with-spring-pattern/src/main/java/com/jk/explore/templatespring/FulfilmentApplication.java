package com.jk.explore.templatespring;

import com.zaxxer.hikari.HikariDataSource;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.dao.DataAccessException;

import java.sql.SQLException;

@SpringBootApplication
public class FulfilmentApplication {

    static final String BAD_SQL = "SELECT order_number FROM ordres";

    static SpringApplicationBuilder builder() {
        return new SpringApplicationBuilder(FulfilmentApplication.class).web(WebApplicationType.NONE);
    }

    static int connectionsInUse(ConfigurableApplicationContext ctx) {
        return ctx.getBean(HikariDataSource.class).getHikariPoolMXBean().getActiveConnections();
    }

    public static void main(String[] args) throws Exception {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    static void one() throws Exception {
        System.out.println("ONE. Plain JDBC leaks on the error path.");
        try (ConfigurableApplicationContext ctx = builder().run()) {
            OrderRepository repo = ctx.getBean(OrderRepository.class);
            System.out.println("  a good query returns " + repo.orderNumbersByHand("SELECT order_number FROM orders ORDER BY order_number")
                    + ". connections in use afterwards: " + connectionsInUse(ctx) + ".");
            try {
                repo.orderNumbersByHand(BAD_SQL);
            } catch (SQLException e) {
                System.out.println("  a query with a typo throws " + e.getClass().getSimpleName() + ". connections in use afterwards: " + connectionsInUse(ctx) + ".");
            }
            System.out.println("  the pool has two connections, so a second typo leaves one, and a third waits for a connection that never comes back.");
        }
    }

    static void two() {
        System.out.println("TWO. The template closes on every path.");
        try (ConfigurableApplicationContext ctx = builder().run()) {
            OrderRepository repo = ctx.getBean(OrderRepository.class);
            System.out.println("  a good query returns " + repo.orderNumbers("SELECT order_number FROM orders ORDER BY order_number")
                    + ". connections in use afterwards: " + connectionsInUse(ctx) + ".");
            for (int i = 0; i < 3; i++) {
                try {
                    repo.orderNumbers(BAD_SQL);
                } catch (DataAccessException e) {
                    // expected: the point is what happens to the connection
                }
            }
            System.out.println("  the same typo, three times: connections in use afterwards: " + connectionsInUse(ctx) + ".");
        }
    }

    static void three() {
        System.out.println("THREE. What is ours, and what is not.");
        try (ConfigurableApplicationContext ctx = builder().run()) {
            OrderRepository repo = ctx.getBean(OrderRepository.class);
            System.out.println("  asha's orders: " + repo.ordersOf("asha"));
            System.out.println("  we wrote one lambda, which turns a row into an Order. The template opened the");
            System.out.println("  connection, prepared the statement, bound the customer, ran it, walked the rows,");
            System.out.println("  and closed everything.");
        }
    }

    static void four() throws Exception {
        System.out.println("FOUR. Exceptions, translated.");
        try (ConfigurableApplicationContext ctx = builder().run()) {
            OrderRepository repo = ctx.getBean(OrderRepository.class);
            try {
                repo.orderNumbersByHand(BAD_SQL);
            } catch (SQLException e) {
                System.out.println("  by hand: " + e.getClass().getSimpleName() + ", a checked exception, SQL state " + e.getSQLState() + ".");
            }
            try {
                repo.orderNumbers(BAD_SQL);
            } catch (DataAccessException e) {
                System.out.println("  template: " + e.getClass().getSimpleName() + ", unchecked, the same on every database.");
            }
            try {
                repo.insert("ORD-000001", "asha", 100);
            } catch (DataAccessException e) {
                System.out.println("  a repeated order number: " + e.getClass().getSimpleName() + ".");
            }
        }
    }

    static void five() {
        System.out.println("FIVE. What the template does not decide for you.");
        try (ConfigurableApplicationContext ctx = builder().run()) {
            OrderRepository repo = ctx.getBean(OrderRepository.class);
            try {
                repo.find("ORD-999999");
            } catch (DataAccessException e) {
                System.out.println("  one row expected, none found: " + e.getClass().getSimpleName() + ".");
            }
            try {
                repo.findByCustomerExpectingOne("asha");
            } catch (DataAccessException e) {
                System.out.println("  one row expected, two found: " + e.getClass().getSimpleName() + ".");
            }
            System.out.println("  the fixed steps are the template's. What counts as a missing row is a decision it made for you.");
        }
    }

    static void six() {
        System.out.println("SIX. A transaction is a template too.");
        try (ConfigurableApplicationContext ctx = builder().run()) {
            OrderRepository repo = ctx.getBean(OrderRepository.class);
            Checkout checkout = ctx.getBean(Checkout.class);
            System.out.println("  before: " + repo.count() + " orders, " + repo.onHand("MUG-BLUE") + " mugs on hand.");
            checkout.placeAndReserve("ORD-000004", "carol", 998, "MUG-BLUE", 2);
            System.out.println("  after a good checkout: " + repo.count() + " orders, " + repo.onHand("MUG-BLUE") + " mug on hand.");
            try {
                checkout.placeAndReserve("ORD-000005", "dev", 1996, "MUG-BLUE", 4);
            } catch (DataAccessException e) {
                System.out.println("  a checkout for 4 mugs fails: " + e.getClass().getSimpleName() + ".");
            }
            System.out.println("  after it: " + repo.count() + " orders, " + repo.onHand("MUG-BLUE") + " mug on hand. the order row was rolled back.");
        }
    }
}
