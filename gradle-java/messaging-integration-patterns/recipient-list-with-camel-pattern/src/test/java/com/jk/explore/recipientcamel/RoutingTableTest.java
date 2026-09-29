package com.jk.explore.recipientcamel;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import org.junit.jupiter.api.Test;

class RoutingTableTest {

    private final RoutingTable table = new RoutingTable();

    @Test
    void oneWarehouseListedOncePerOrder() {
        assertEquals("direct:north", table.recipients(new Order("X", List.of("kitchen", "kitchen"), 100, false)));
    }

    @Test
    void exactlyFiveHundredIsNotReviewed() {
        assertEquals("direct:cold-store", table.recipients(new Order("X", List.of("chilled"), 50000, false)));
    }
}
