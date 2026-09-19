package com.jk.explore.aggregate;

import com.jk.explore.aggregate.domain.*;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class OrderAggregateTest {

    private static Order order() {
        return new Order(new OrderId("O"), new CustomerId("c"));
    }

    @Test
    void quantityMustBeBetweenOneAndTen() {
        Order o = order();
        assertThrows(InvariantViolated.class, () -> o.addLine("A", Money.pounds(1), 0));
        assertThrows(InvariantViolated.class, () -> o.addLine("A", Money.pounds(1), 11));
        o.addLine("A", Money.pounds(1), 10);
        assertEquals(10, o.lines().get(0).quantity());
    }

    @Test
    void anItemAppearsOnOneLineAndQuantitiesMerge() {
        Order o = order();
        o.addLine("A", Money.pounds(1), 4);
        o.addLine("A", Money.pounds(1), 5);
        assertEquals(1, o.lines().size());
        assertEquals(9, o.lines().get(0).quantity());
        assertThrows(InvariantViolated.class, () -> o.addLine("A", Money.pounds(1), 2));
        assertEquals(9, o.lines().get(0).quantity());
    }

    @Test
    void theCreditLimitIsAnInvariantOverAllTheLines() {
        Order o = order();
        o.addLine("A", Money.pounds(300), 3);
        assertThrows(InvariantViolated.class, () -> o.addLine("B", Money.pounds(101), 1));
        o.addLine("B", Money.pounds(100), 1);
        assertEquals(Money.pounds(1000), o.total());
        assertThrows(InvariantViolated.class, () -> o.addLine("A", Money.pounds(300), 1));
        assertEquals(Money.pounds(1000), o.total());
    }

    @Test
    void aPlacedOrderCannotChangeAndAnEmptyOneCannotBePlaced() {
        Order o = order();
        assertThrows(InvariantViolated.class, o::place);
        o.addLine("A", Money.pounds(1), 1);
        o.place();
        assertThrows(InvariantViolated.class, () -> o.addLine("B", Money.pounds(1), 1));
    }

    @Test
    void theLineListCannotBeChangedFromOutside() {
        Order o = order();
        o.addLine("A", Money.pounds(1), 1);
        assertThrows(UnsupportedOperationException.class, () -> o.lines().clear());
        assertThrows(UnsupportedOperationException.class, () -> o.lines().add(o.lines().get(0)));
    }

    @Test
    void aCopyIsIndependent() {
        Order o = order();
        o.addLine("A", Money.pounds(1), 1);
        Order copy = o.copy();
        copy.addLine("B", Money.pounds(1), 1);
        assertEquals(1, o.lines().size());
        assertEquals(2, copy.lines().size());
    }
}
