package com.jk.explore.decorator;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;

class InsuranceDecoratorTest {

    @Test
    void addsAPercentagePremiumOfWhateverItWraps() {
        PricedItem product = new Product("Wireless Headphones", new BigDecimal("79.99"));
        PricedItem insured = new InsuranceDecorator(product);

        assertEquals(new BigDecimal("81.59"), insured.cost());
        assertEquals("Wireless Headphones, insured", insured.description());
    }

    @Test
    void pricesOffWhateverItWrapsNotJustTheBaseProduct() {
        PricedItem product = new Product("Wireless Headphones", new BigDecimal("79.99"));
        PricedItem giftWrapped = new GiftWrapDecorator(product);
        PricedItem giftWrappedInsured = new InsuranceDecorator(giftWrapped);

        assertEquals(new BigDecimal("85.16"), giftWrappedInsured.cost());
        assertEquals("Wireless Headphones, gift-wrapped, insured", giftWrappedInsured.description());
    }
}
