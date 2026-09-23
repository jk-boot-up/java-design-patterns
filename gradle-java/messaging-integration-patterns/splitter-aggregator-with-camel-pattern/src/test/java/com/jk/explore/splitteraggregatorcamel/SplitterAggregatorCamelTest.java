package com.jk.explore.splitteraggregatorcamel;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Nothing here sleeps for a fixed length of time. The route steps are synchronous, so a send has finished
 * when it returns; the one wait in the whole file is the aggregator's deadline, and that is a bounded wait
 * on a real event which fails loudly rather than hanging.
 */
class SplitterAggregatorCamelTest {

    private final Store store = new Store();

    @AfterEach
    void stop() {
        store.close();
    }

    private List<Shipment> split(String orderId) {
        store.collected.clear();
        store.checkout(Store.order(orderId), "direct:collect", "");
        return new ArrayList<>(store.collected);
    }

    @Test
    void theSplitterMakesOneShipmentPerLineEachCarryingTheOrderNumberAndItsPlace() {
        List<Shipment> shipments = split("ORD-1");
        assertEquals(3, shipments.size());
        for (int i = 0; i < 3; i++) {
            Shipment s = shipments.get(i);
            assertEquals("ORD-1", s.orderId());
            assertEquals(i + 1, s.index());
            assertEquals(3, s.of());
            assertEquals(Store.WAREHOUSES.get(i), s.warehouse());
        }
        assertEquals(List.of(1598, 24999, 1745), shipments.stream().map(Shipment::pence).toList());
    }

    @Test
    void shipmentsArrivingJumbledComeBackInLineOrderAndCompleteBySize() {
        List<Shipment> shipments = split("ORD-1");
        for (int i : new int[]{3, 1, 2}) {
            store.deliver(shipments.get(i - 1), "direct:gather");
        }
        Gathered done = store.results.next();
        assertEquals("size", done.completedBy());
        assertTrue(done.order().complete());
        assertEquals(List.of("2 x MUG-BLUE from Leeds", "1 x ESP-001 from Reading", "5 x TEA-050 from Glasgow"),
                done.order().contents());
        assertEquals(28342, done.order().totalPence());
        assertEquals(0, store.routes.ordersOpen());
    }

    @Test
    void anOrderShortOfAShipmentIsHeldAndNothingComesOut() {
        store.checkout(Store.order("ORD-2"), "direct:gather", "Glasgow");
        assertEquals(0, store.results.size());
        assertEquals(1, store.routes.ordersOpen());
    }

    @Test
    void theAggregatorGivesUpAtItsDeadlineAndNamesTheWarehouseThatNeverAnswered() {
        store.checkout(Store.order("ORD-3"), "direct:gather-with-timeout", "Glasgow");
        Gathered done = store.results.next();
        assertEquals("timeout", done.completedBy());
        assertTrue(done.byTimeout());
        assertFalse(done.order().complete());
        assertEquals(2, done.order().count());
        assertEquals(3, done.order().expected());
        assertEquals(List.of("Glasgow"), done.order().missingWarehouses(Store.WAREHOUSES));
        assertEquals(26597, done.order().totalPence());
        assertEquals(0, store.routes.ordersOpenWithTimeout());
    }

    @Test
    void twoOrdersInterleavedAreNeverMixed() {
        List<Shipment> a = split("ORD-A");
        List<Shipment> b = split("ORD-B");
        store.deliver(a.get(0), "direct:gather");
        store.deliver(b.get(0), "direct:gather");
        store.deliver(b.get(1), "direct:gather");
        store.deliver(b.get(2), "direct:gather");
        store.deliver(a.get(1), "direct:gather");
        store.deliver(a.get(2), "direct:gather");
        Gathered first = store.results.next();
        Gathered second = store.results.next();
        assertEquals("ORD-B", first.order().orderId());
        assertEquals("ORD-A", second.order().orderId());
        assertEquals(28342, first.order().totalPence());
        assertEquals(28342, second.order().totalPence());
    }

    @Test
    void aRepeatedShipmentIsCountedOnceAndTheTotalIsProtected() {
        List<Shipment> shipments = split("ORD-4");
        store.deliver(shipments.get(0), "direct:gather");
        store.deliver(shipments.get(1), "direct:gather");
        store.deliver(shipments.get(1), "direct:gather");
        Gathered done = store.results.next();
        assertEquals("size", done.completedBy());
        assertEquals(1, done.order().duplicates());
        assertEquals(2, done.order().count());
        assertEquals(26597, done.order().totalPence());
        assertEquals(51596, done.order().uncheckedTotalPence());
    }

    @Test
    void everyOrderMissingAShipmentStaysInTheAggregatorsMemory() {
        for (int i = 0; i < 100; i++) {
            store.checkout(Store.order("ORD-H-" + i), "direct:gather", "Glasgow");
        }
        assertEquals(100, store.routes.ordersOpen());
        assertEquals(0, store.results.size());
    }

    @Test
    void oneWorkerDoingTheWholeOrderTakesOneStepPerLineOnOneThread() {
        assertEquals(28342, store.onePickerTotal(Store.order("ORD-5")));
        assertEquals(3, store.onePicker.steps());
        assertEquals(1, store.onePicker.threadsUsed());
    }
}
