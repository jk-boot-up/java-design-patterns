package com.jk.explore.decorator;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;

class NaiveProductClassesTest {

    private static final BigDecimal PRICE = new BigDecimal("79.99");

    @Test
    void naiveGiftWrappedProductDuplicatesTheGiftWrapFee() {
        NaiveGiftWrappedProduct naive = new NaiveGiftWrappedProduct("Wireless Headphones", PRICE);

        assertEquals(new BigDecimal("83.49"), naive.cost());
        assertEquals("Wireless Headphones, gift-wrapped", naive.description());
    }

    @Test
    void naiveInsuredProductDuplicatesThePremiumCalculation() {
        NaiveInsuredProduct naive = new NaiveInsuredProduct("Wireless Headphones", PRICE);

        assertEquals(new BigDecimal("81.59"), naive.cost());
        assertEquals("Wireless Headphones, insured", naive.description());
    }

    @Test
    void naiveGiftWrappedInsuredProductNeedsAWholeNewClassForTheCombination() {
        NaiveGiftWrappedInsuredProduct naive =
                new NaiveGiftWrappedInsuredProduct("Wireless Headphones", PRICE);

        assertEquals(new BigDecimal("85.16"), naive.cost());
        assertEquals("Wireless Headphones, gift-wrapped, insured", naive.description());
    }

    @Test
    void matchesTheEquivalentDecoratorStackExactly() {
        PricedItem giftWrappedInsured =
                new InsuranceDecorator(new GiftWrapDecorator(new Product("Wireless Headphones", PRICE)));
        NaiveGiftWrappedInsuredProduct naive =
                new NaiveGiftWrappedInsuredProduct("Wireless Headphones", PRICE);

        assertEquals(giftWrappedInsured.cost(), naive.cost());
        assertEquals(giftWrappedInsured.description(), naive.description());
    }
}
