package com.jk.explore.authorization;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class PolicyTest {

    private final Policy policy = Policy.shop();
    private final Order order = new Order("O1", "ben", 50);

    @Test
    void ownerMayCancel() {
        assertTrue(policy.decide(Request.of(new User("ben", "CUSTOMER"), "order:cancel", order)).allowed());
    }

    @Test
    void supportMayNotCancel() {
        assertFalse(policy.decide(Request.of(new User("sam", "SUPPORT"), "order:cancel", order)).allowed());
    }

    @Test
    void supportRefundLimitIsInclusive() {
        assertTrue(policy.decide(new Request(new User("sam", "SUPPORT"), "refund:issue", order, 100)).allowed());
    }

    @Test
    void customersCannotRefund() {
        assertFalse(policy.decide(new Request(new User("ben", "CUSTOMER"), "refund:issue", order, 1)).allowed());
    }

    @Test
    void unknownRoleGetsNothing() {
        assertFalse(policy.decide(Request.of(new User("x", "GUEST"), "order:view", order)).allowed());
    }
}
