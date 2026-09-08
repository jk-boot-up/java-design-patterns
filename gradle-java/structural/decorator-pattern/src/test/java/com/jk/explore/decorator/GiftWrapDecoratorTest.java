package com.jk.explore.decorator;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;

class GiftWrapDecoratorTest {

    @Test
    void addsAFlatFeeAndAppendsToTheDescription() {
        PricedItem product = new Product("Wireless Headphones", new BigDecimal("79.99"));
        PricedItem giftWrapped = new GiftWrapDecorator(product);

        assertEquals(new BigDecimal("83.49"), giftWrapped.cost());
        assertEquals("Wireless Headphones, gift-wrapped", giftWrapped.description());
    }
}
