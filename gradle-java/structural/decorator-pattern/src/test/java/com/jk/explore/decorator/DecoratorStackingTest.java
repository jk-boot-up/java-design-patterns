package com.jk.explore.decorator;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;

class DecoratorStackingTest {

    private final PricedItem product = new Product("Wireless Headphones", new BigDecimal("79.99"));

    @Test
    void decoratorsCanBeStackedThreeDeep() {
        PricedItem giftWrapped = new GiftWrapDecorator(product);
        PricedItem giftWrappedInsured = new InsuranceDecorator(giftWrapped);
        PricedItem giftWrappedInsuredExpress = new ExpressHandlingDecorator(giftWrappedInsured);

        assertEquals(new BigDecimal("95.15"), giftWrappedInsuredExpress.cost());
        assertEquals("Wireless Headphones, gift-wrapped, insured, express handling",
                giftWrappedInsuredExpress.description());
    }

    @Test
    void wrappingOrderChangesTheTotalWhenAPercentageDecoratorIsInvolved() {
        PricedItem giftWrappedThenInsured = new InsuranceDecorator(new GiftWrapDecorator(product));
        PricedItem insuredThenGiftWrapped = new GiftWrapDecorator(new InsuranceDecorator(product));

        assertEquals(new BigDecimal("85.16"), giftWrappedThenInsured.cost());
        assertEquals(new BigDecimal("85.09"), insuredThenGiftWrapped.cost());
        assertNotEquals(giftWrappedThenInsured.cost(), insuredThenGiftWrapped.cost());
    }
}
