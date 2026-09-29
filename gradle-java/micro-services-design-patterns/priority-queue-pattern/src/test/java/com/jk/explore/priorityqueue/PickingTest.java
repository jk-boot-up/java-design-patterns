package com.jk.explore.priorityqueue;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class PickingTest {

    @Test
    void fifoPicksInArrivalOrder() {
        Map<String, Integer> m = Picking.run(Picking.fifo(), PriorityQueueDemo.morning(100), 20, 0);
        assertEquals(10, PriorityQueueDemo.lastSameDay(m));
    }

    @Test
    void priorityPicksSameDayFirst() {
        Map<String, Integer> m = Picking.run(Picking.priority(), PriorityQueueDemo.morning(100), 20, 0);
        assertEquals(1, PriorityQueueDemo.lastSameDay(m));
    }

    @Test
    void reservedShareServesStandard() {
        List<Order> l = List.of(new Order("S", false, 0, 0), new Order("U", true, 0, 1));
        Map<String, Integer> m = Picking.run(Picking.priority(), l, 1, 1);
        assertEquals(0, m.get("S"));
    }
}
