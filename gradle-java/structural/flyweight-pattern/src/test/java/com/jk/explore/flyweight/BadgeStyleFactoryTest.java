package com.jk.explore.flyweight;

import org.junit.jupiter.api.Test;

import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertTrue;

class BadgeStyleFactoryTest {

    @Test
    void styleForReturnsSameInstanceForSameType() {
        BadgeStyle first = BadgeStyleFactory.styleFor(BadgeType.NEW);
        BadgeStyle second = BadgeStyleFactory.styleFor(BadgeType.NEW);

        assertSame(first, second);
    }

    @Test
    void styleForReturnsDifferentInstancesForDifferentTypes() {
        BadgeStyle sale = BadgeStyleFactory.styleFor(BadgeType.SALE);
        BadgeStyle bestseller = BadgeStyleFactory.styleFor(BadgeType.BESTSELLER);

        assertNotSame(sale, bestseller);
    }

    @Test
    void repeatedLookupsForAnAlreadyBuiltTypeCreateNoNewInstances() {
        BadgeStyleFactory.styleFor(BadgeType.LOW_STOCK);
        int before = BadgeStyleFactory.instancesCreated();

        for (int i = 0; i < 1_000; i++) {
            BadgeStyleFactory.styleFor(BadgeType.LOW_STOCK);
        }

        assertEquals(before, BadgeStyleFactory.instancesCreated());
    }

    @Test
    void everyBadgeTypeEndsUpWithExactlyOneCachedInstance() {
        for (BadgeType type : BadgeType.values()) {
            BadgeStyleFactory.styleFor(type);
        }

        assertTrue(BadgeStyleFactory.instancesCreated() <= BadgeType.values().length,
                "no more than one instance should ever exist per badge type");
    }

    @Test
    void concurrentLookupsForTheSameTypeAllReceiveTheSameInstance() throws InterruptedException {
        int threadCount = 30;
        CountDownLatch ready = new CountDownLatch(threadCount);
        CountDownLatch go = new CountDownLatch(1);
        CountDownLatch done = new CountDownLatch(threadCount);
        Set<BadgeStyle> seen = ConcurrentHashMap.newKeySet();
        ExecutorService pool = Executors.newFixedThreadPool(threadCount);

        try {
            for (int i = 0; i < threadCount; i++) {
                pool.submit(() -> {
                    ready.countDown();
                    try {
                        go.await();
                        seen.add(BadgeStyleFactory.styleFor(BadgeType.BESTSELLER));
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    } finally {
                        done.countDown();
                    }
                });
            }

            ready.await();
            go.countDown();
            assertTrue(done.await(10, TimeUnit.SECONDS));
        } finally {
            pool.shutdown();
        }

        assertEquals(1, seen.size(), "every thread should observe the same shared BadgeStyle");
    }
}
