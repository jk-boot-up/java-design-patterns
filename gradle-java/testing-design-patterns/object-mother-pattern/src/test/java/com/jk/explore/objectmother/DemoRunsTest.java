package com.jk.explore.objectmother;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", ObjectMotherDemo.run());

    @Test
    void acts() {
        assertTrue(all.contains("3 constructors, 8 values, to test one rule: shipping 4.99"));
        assertTrue(all.contains("TestOrders.vip():           shipping 0.00"));
        assertTrue(all.contains("TestOrders.international(): shipping 15.00"));
        assertTrue(all.contains("3 yes-or-no details: 8 methods"));
        assertTrue(all.contains("one more detail and it is 16"));
        assertTrue(all.contains("shippedTo(\"FR\").build(): shipping 15.00"));
        assertTrue(all.contains("giftWrapped().build():   shipping 2.00"));
        assertTrue(all.contains("then:  shipping 0.00"));
        assertTrue(all.contains("lowers the default to 30.00: shipping 4.99"));
    }
}
