package com.jk.explore.lenses;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", LensesDemo.run());

    @Test
    void acts() {
        assertTrue(all.contains("result: Address[street=Leeds, city=1 High Street, postcode=LS2 7HY]"));
        assertTrue(all.contains("ADDRESS_POSTCODE.get(address):            LS1 4AP"));
        assertTrue(all.contains("the original is unchanged:                Address[street=1 High Street, city=Leeds, postcode=LS1 4AP]"));
        assertTrue(all.contains("ORDER_POSTCODE.set(order, \"LS2 7HY\"): Address[street=1 High Street, city=Leeds, postcode=LS2 7HY]"));
        assertTrue(all.contains("ORDER_POSTCODE.modify(upper):   LS2 7HY"));
        assertTrue(all.contains("city=York, postcode=YO1 7HH"));
        assertTrue(all.contains("lines are the same list: true"));
    }
}
