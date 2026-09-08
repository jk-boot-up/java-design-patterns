package com.jk.explore.decorator;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ProductTest {

    @Test
    void reportsItsOwnPriceAndName() {
        Product product = new Product("Wireless Headphones", new BigDecimal("79.99"));

        assertEquals(new BigDecimal("79.99"), product.cost());
        assertEquals("Wireless Headphones", product.description());
    }
}
