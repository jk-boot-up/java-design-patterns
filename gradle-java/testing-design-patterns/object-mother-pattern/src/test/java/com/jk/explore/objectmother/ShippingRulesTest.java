package com.jk.explore.objectmother;

import static com.jk.explore.objectmother.OrderBuilder.anOrder;
import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

/**
 * The shipping rules, tested the way the pattern recommends: each test names only what it relies on.
 */
class ShippingRulesTest {

    @Test
    void ukOrdersOverFiftyShipFree() {
        assertEquals(0.00, ShippingRules.cost(anOrder().totalling(60).build()));
    }

    @Test
    void smallUkOrdersPay() {
        assertEquals(4.99, ShippingRules.cost(anOrder().totalling(20).build()));
    }

    @Test
    void vipsShipFreeInTheUk() {
        assertEquals(0.00, ShippingRules.cost(anOrder().vip().totalling(20).build()));
    }

    @Test
    void ordersAbroadPayEvenForVips() {
        assertEquals(15.00, ShippingRules.cost(anOrder().vip().shippedTo("FR").build()));
    }

    @Test
    void giftWrapAddsTwo() {
        assertEquals(6.99, ShippingRules.cost(anOrder().totalling(20).giftWrapped().build()), 0.001);
    }

    @Test
    void motherOrdersAreReady() {
        assertEquals(15.00, ShippingRules.cost(TestOrders.international()));
    }
}
