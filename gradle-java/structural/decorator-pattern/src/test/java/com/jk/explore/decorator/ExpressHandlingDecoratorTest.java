package com.jk.explore.decorator;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ExpressHandlingDecoratorTest {

    @Test
    void addsAFlatFeeAndAppendsToTheDescription() {
        PricedItem product = new Product("Wireless Headphones", new BigDecimal("79.99"));
        PricedItem express = new ExpressHandlingDecorator(product);

        assertEquals(new BigDecimal("89.98"), express.cost());
        assertEquals("Wireless Headphones, express handling", express.description());
    }
}
