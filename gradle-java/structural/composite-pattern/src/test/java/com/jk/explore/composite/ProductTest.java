package com.jk.explore.composite;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ProductTest {

    @Test
    void totalPriceIsItsOwnPrice() {
        Product phone = new Product("Phone", new BigDecimal("599.99"));

        assertEquals(new BigDecimal("599.99"), phone.totalPrice());
    }

    @Test
    void productCountIsAlwaysOne() {
        Product phone = new Product("Phone", new BigDecimal("599.99"));

        assertEquals(1, phone.productCount());
    }

    @Test
    void nameReturnsTheGivenName() {
        Product phone = new Product("Phone", new BigDecimal("599.99"));

        assertEquals("Phone", phone.name());
    }
}
