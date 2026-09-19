package com.jk.explore.delegation;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.jk.explore.delegation.naive.PremiumGiftOrder;
import org.junit.jupiter.api.Test;

class DelegationTest {

    @Test
    void theDelegatedAndInheritedOrdersAgree() {
        Order order = new Order(10000, 2, PricingRule.inOrder(PricingRule.premium(), PricingRule.giftWrap()));
        assertEquals(new PremiumGiftOrder(10000, 2).total(), order.total());
        assertEquals(9600, order.total());
    }

    @Test
    void eachRuleGivesItsOwnTotal() {
        assertEquals(10000, new Order(10000, 2, PricingRule.NONE).total());
        assertEquals(9000, new Order(10000, 2, PricingRule.premium()).total());
        assertEquals(10600, new Order(10000, 2, PricingRule.giftWrap()).total());
    }

    @Test
    void theRuleCanBeSwappedOnTheSameObject() {
        Order order = new Order(10000, 2, PricingRule.NONE);
        assertEquals(10000, order.total());
        order.useRule(PricingRule.premium());
        assertEquals(9000, order.total());
    }

    @Test
    void theRuleSeesTheOrderItIsCalledFor() {
        assertEquals(10600, new Order(10000, 2, PricingRule.giftWrap()).total());
        assertEquals(10900, new Order(10000, 3, PricingRule.giftWrap()).total());
    }

    @Test
    void eachHelperCostsACall() {
        PricingRule.CALLS.set(0);
        new Order(10000, 2, PricingRule.inOrder(PricingRule.NONE, PricingRule.premium(), PricingRule.giftWrap())).total();
        assertEquals(3, PricingRule.CALLS.get());
    }

    @Test
    void forwardingNeedsAMethodForEachMethod() {
        assertEquals(Shipping.class.getMethods().length, OrderWithShipping.class.getDeclaredMethods().length);
    }
}
