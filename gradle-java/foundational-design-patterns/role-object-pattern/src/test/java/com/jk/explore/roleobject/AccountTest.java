package com.jk.explore.roleobject;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class AccountTest {

    private final Account a = new Account("C-1", "Tom");

    @Test
    void missingRoleIsEmpty() {
        assertTrue(a.as(Roles.Seller.class).isEmpty());
    }

    @Test
    void roleKnowsItsAccount() {
        Roles.Buyer b = a.addRole(new Roles.Buyer(a));
        assertSame(a, b.account());
        assertSame(b, a.as(Roles.Buyer.class).orElseThrow());
    }

    @Test
    void removingOneRoleKeepsTheOthers() {
        a.addRole(new Roles.Buyer(a)).placeOrder("X");
        a.addRole(new Roles.Seller(a, "Tom's"));
        a.removeRole(Roles.Seller.class);
        assertEquals(1, a.as(Roles.Buyer.class).orElseThrow().orders().size());
        assertTrue(a.as(Roles.Seller.class).isEmpty());
    }

    @Test
    void affiliateEarnsPercent() {
        Roles.Affiliate af = a.addRole(new Roles.Affiliate(a, 5));
        af.referred(4000);
        assertEquals(200, af.earnedPence());
    }

    @Test
    void subclassMixesGrowFast() {
        assertEquals(7, Subclasses.classesNeeded(3));
        assertEquals(15, Subclasses.classesNeeded(4));
    }
}
