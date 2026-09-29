package com.jk.explore.roleobject;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", RoleObjectDemo.run());

    @Test
    void subclasses() {
        assertTrue(all.contains("orders on the new object: 0; same person: false"));
        assertTrue(all.contains("in any mix: 7 classes"));
    }

    @Test
    void roles() {
        assertTrue(all.contains("Priya (C-17) plays [Buyer, Seller]"));
        assertTrue(all.contains("orders still on the account: 12"));
        assertTrue(all.contains("Priya's Pottery lists hand-thrown mug"));
        assertTrue(all.contains("earned £5.00"));
    }

    @Test
    void dropRole() {
        assertTrue(all.contains("roles now [Buyer, Affiliate]"));
        assertTrue(all.contains("refused, Priya is not a seller"));
        assertTrue(all.contains("she can still buy: 13 orders"));
    }
}
