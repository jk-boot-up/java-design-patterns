package com.jk.explore.singletable;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.List;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class ProductTableTest {

    private Connection c;
    private ProductTable t;

    @BeforeEach
    void open() throws SQLException {
        c = DriverManager.getConnection("jdbc:h2:mem:t" + System.nanoTime());
        t = new ProductTable(c);
        t.create();
    }

    @AfterEach
    void close() throws SQLException {
        c.close();
    }

    @Test
    void eachRowBecomesItsOwnClass() throws SQLException {
        List<Products.Product> all = t.all();
        assertInstanceOf(Products.Book.class, all.get(0));
        assertInstanceOf(Products.Electronics.class, all.get(1));
        assertInstanceOf(Products.Food.class, all.get(3));
    }

    @Test
    void oneQueryForAllTypes() throws SQLException {
        assertEquals(List.of("breakfast tea", "desk lamp"), t.under(1000).stream().map(Products.Product::name).toList());
        assertEquals(1, t.queries());
    }

    @Test
    void typeSpecificFieldsSurviveTheRoundTrip() throws SQLException {
        assertEquals(new Products.Food("TEA-1", "breakfast tea", 400, "2027-03-01"), t.all().get(3));
    }

    @Test
    void giftCardsAfterAddingTheColumn() throws SQLException {
        t.addGiftCards();
        t.insert(new Products.GiftCard("GIFT-1", "gift card", 5000, 5000));
        assertEquals(new Products.GiftCard("GIFT-1", "gift card", 5000, 5000), t.all().get(1));
    }
}
