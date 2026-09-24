package com.jk.explore.loadlevelingsqs;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import org.junit.jupiter.api.Test;

/** The parts that need no container: the order ids and the warehouse's parcel count. */
class PlainPartsTest {

    @Test
    void aBurstIsNumberedOnFromItsFirstOrder() {
        List<String> ids = Checkout.orders(1001, 100);
        assertEquals(100, ids.size());
        assertEquals("ORD-1001", ids.get(0));
        assertEquals("ORD-1100", ids.get(99));
    }

    @Test
    void theWarehouseCountsEveryParcelSoAnOrderPackedTwiceShows() {
        Warehouse warehouse = new Warehouse();
        warehouse.pack("ORD-3001");
        warehouse.pack("ORD-3001");
        warehouse.pack("ORD-3002");
        assertEquals(2, warehouse.parcelsFor("ORD-3001"));
        assertEquals(1, warehouse.parcelsFor("ORD-3002"));
        assertEquals(0, warehouse.parcelsFor("ORD-9999"));
        assertEquals(2, warehouse.ordersPacked());
        assertEquals(1, warehouse.packedTwiceOrMore());
    }

    @Test
    void sqsTakesAtMostTenOrdersToARequest() {
        assertEquals(10, OrderQueue.MOST_PER_REQUEST);
    }
}
