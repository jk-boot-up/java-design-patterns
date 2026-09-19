package com.jk.explore.producerconsumer;

import com.jk.explore.producerconsumer.domain.Order;
import com.jk.explore.producerconsumer.pattern.BoundedOrderQueue;
import org.junit.jupiter.api.Test;

import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class BoundedOrderQueueTest {

    @Test
    void putAndTakeReturnTheSameOrder() throws InterruptedException {
        BoundedOrderQueue queue = new BoundedOrderQueue(2);
        Order order = new Order("ord-1", "BNS-220");

        queue.put(order);

        assertEquals(1, queue.size());
        assertEquals(order, queue.take());
        assertEquals(0, queue.size());
    }

    @Test
    void offerRejectsWhenFullAndNoConsumerIsTaking() throws InterruptedException {
        BoundedOrderQueue queue = new BoundedOrderQueue(1);
        queue.put(new Order("ord-1", "BNS-220"));

        assertTrue(queue.isFull());
        boolean accepted = queue.offer(new Order("ord-2", "BNS-220"), 50, TimeUnit.MILLISECONDS);

        assertFalse(accepted, "a full queue with nobody consuming must reject, not grow");
        assertEquals(1, queue.size());
    }

    @Test
    void offerSucceedsOnceRoomAppears() throws InterruptedException {
        BoundedOrderQueue queue = new BoundedOrderQueue(1);
        queue.put(new Order("ord-1", "BNS-220"));

        Thread consumer = new Thread(() -> {
            try {
                queue.take();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        consumer.start();

        boolean accepted = queue.offer(new Order("ord-2", "BNS-220"), 2, TimeUnit.SECONDS);

        assertTrue(accepted, "room freed up within the patience window, so this must succeed");
        consumer.join(2_000);
    }
}
