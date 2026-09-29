package com.jk.explore.statetable;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;
import java.util.Set;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.EnumSource;

class TransitionTableTest {

    private final TransitionTable table = TransitionTable.orders();

    @Test
    void happyPath() {
        Order o = new Order("x", table).apply(Action.PAY).apply(Action.SHIP).apply(Action.DELIVER);
        assertEquals(List.of(Status.PLACED, Status.PAID, Status.SHIPPED, Status.DELIVERED), o.history());
    }

    @ParameterizedTest
    @EnumSource(Action.class)
    void nothingHappensToADeliveredOrder(Action action) {
        Order o = new Order("x", table).apply(Action.PAY).apply(Action.SHIP).apply(Action.DELIVER);
        assertThrows(IllegalStateException.class, () -> o.apply(action));
        assertEquals(Status.DELIVERED, o.status());
    }

    @Test
    void refusalNamesTheMove() {
        Order o = new Order("x", table);
        IllegalStateException e = assertThrows(IllegalStateException.class, () -> o.apply(Action.SHIP));
        assertEquals("cannot ship a PLACED order", e.getMessage());
    }

    @Test
    void allowedGivesTheButtons() {
        assertEquals(Set.of(Action.PAY, Action.CANCEL), table.allowed(Status.PLACED));
        assertEquals(Set.of(), table.allowed(Status.REFUNDED));
    }

    @Test
    void addingARowAddsAMove() {
        table.allow(Status.DELIVERED, Action.RETURN, Status.RETURNED);
        assertEquals(6, table.transitions());
        assertEquals(Set.of(Action.RETURN), table.allowed(Status.DELIVERED));
    }

    @Test
    void ifElseVersionHasTheBugs() {
        IfElseOrder o = new IfElseOrder();
        o.pay();
        o.refund();
        o.refund();
        assertEquals(2, o.refunds());
    }
}
