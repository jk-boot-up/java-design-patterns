package com.jk.explore.templatespring;

import org.junit.jupiter.api.Test;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.dao.IncorrectResultSizeDataAccessException;
import org.springframework.jdbc.BadSqlGrammarException;

import java.sql.SQLException;

import static org.junit.jupiter.api.Assertions.*;

class TemplateBeanTest {

    @Test
    void handWrittenJdbcLeaksAConnectionOnTheErrorPath() {
        try (ConfigurableApplicationContext ctx = FulfilmentApplication.builder().run()) {
            OrderRepository repo = ctx.getBean(OrderRepository.class);
            assertThrows(SQLException.class, () -> repo.orderNumbersByHand(FulfilmentApplication.BAD_SQL));
            assertEquals(1, FulfilmentApplication.connectionsInUse(ctx));
        }
    }

    @Test
    void handWrittenJdbcIsFineOnTheHappyPath() throws Exception {
        try (ConfigurableApplicationContext ctx = FulfilmentApplication.builder().run()) {
            assertEquals(3, ctx.getBean(OrderRepository.class).orderNumbersByHand("SELECT order_number FROM orders").size());
            assertEquals(0, FulfilmentApplication.connectionsInUse(ctx));
        }
    }

    @Test
    void templateReleasesTheConnectionEvenWhenTheQueryFails() {
        try (ConfigurableApplicationContext ctx = FulfilmentApplication.builder().run()) {
            OrderRepository repo = ctx.getBean(OrderRepository.class);
            for (int i = 0; i < 5; i++) {
                assertThrows(BadSqlGrammarException.class, () -> repo.orderNumbers(FulfilmentApplication.BAD_SQL));
            }
            assertEquals(0, FulfilmentApplication.connectionsInUse(ctx));
        }
    }

    @Test
    void rowMapperBuildsOrders() {
        try (ConfigurableApplicationContext ctx = FulfilmentApplication.builder().run()) {
            var orders = ctx.getBean(OrderRepository.class).ordersOf("asha");
            assertEquals(2, orders.size());
            assertEquals(new Order("ORD-000001", "asha", 2499), orders.get(0));
        }
    }

    @Test
    void exceptionsAreTranslated() {
        try (ConfigurableApplicationContext ctx = FulfilmentApplication.builder().run()) {
            assertThrows(DuplicateKeyException.class, () -> ctx.getBean(OrderRepository.class).insert("ORD-000001", "x", 1));
        }
    }

    @Test
    void missingAndAmbiguousRowsAreErrorsNotNulls() {
        try (ConfigurableApplicationContext ctx = FulfilmentApplication.builder().run()) {
            OrderRepository repo = ctx.getBean(OrderRepository.class);
            assertThrows(EmptyResultDataAccessException.class, () -> repo.find("NOPE"));
            assertThrows(IncorrectResultSizeDataAccessException.class, () -> repo.findByCustomerExpectingOne("asha"));
        }
    }

    @Test
    void failedCheckoutIsRolledBackWhole() {
        try (ConfigurableApplicationContext ctx = FulfilmentApplication.builder().run()) {
            OrderRepository repo = ctx.getBean(OrderRepository.class);
            Checkout checkout = ctx.getBean(Checkout.class);
            checkout.placeAndReserve("ORD-000004", "carol", 998, "MUG-BLUE", 2);
            assertEquals(4, repo.count());
            assertEquals(1, repo.onHand("MUG-BLUE"));
            assertThrows(org.springframework.dao.DataAccessException.class, () -> checkout.placeAndReserve("ORD-000005", "dev", 1, "MUG-BLUE", 4));
            assertEquals(4, repo.count());
            assertEquals(1, repo.onHand("MUG-BLUE"));
        }
    }
}
