package com.jk.explore.currying;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class ShippingTest {

    @Test
    void curriedMatchesPlainForEveryCombination() {
        for (Zone z : Zone.values()) {
            for (Service s : Service.values()) {
                for (double kg : new double[] {0, 1.5, 30}) {
                    assertEquals(Shipping.price(z, s, kg), Shipping.CURRIED.apply(z).apply(s).apply(kg));
                }
            }
        }
    }

    @Test
    void curryFixesTheFirstArgument() {
        assertEquals("a-b", Shipping.<String, String, String>curry((x, y) -> x + "-" + y).apply("a").apply("b"));
    }
}
