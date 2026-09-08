package com.jk.explore.singleton;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.lang.reflect.Constructor;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class OrderSequenceGeneratorTest {

    @Test
    void instanceIsSharedAcrossReferences() {
        OrderSequenceGenerator first = OrderSequenceGenerator.INSTANCE;
        OrderSequenceGenerator second = OrderSequenceGenerator.INSTANCE;

        assertSame(first, second);
    }

    @Test
    void nextOrderNumberMatchesExpectedFormat() {
        String orderNumber = OrderSequenceGenerator.INSTANCE.nextOrderNumber();

        assertTrue(orderNumber.matches("ORD-\\d{6}"), orderNumber);
    }

    @Test
    void nextOrderNumberNeverRepeats() {
        String first = OrderSequenceGenerator.INSTANCE.nextOrderNumber();
        String second = OrderSequenceGenerator.INSTANCE.nextOrderNumber();
        String third = OrderSequenceGenerator.INSTANCE.nextOrderNumber();

        assertTrue(numericPart(first) < numericPart(second));
        assertTrue(numericPart(second) < numericPart(third));
    }

    @Test
    void reflectionCannotCreateASecondInstance() throws NoSuchMethodException {
        Constructor<OrderSequenceGenerator> constructor =
                OrderSequenceGenerator.class.getDeclaredConstructor(String.class, int.class);
        constructor.setAccessible(true);

        assertThrows(IllegalArgumentException.class,
                () -> constructor.newInstance("FORGED", 99));
    }

    @Test
    void serializationReturnsTheSameInstance() throws Exception {
        ByteArrayOutputStream bytes = new ByteArrayOutputStream();
        try (ObjectOutputStream out = new ObjectOutputStream(bytes)) {
            out.writeObject(OrderSequenceGenerator.INSTANCE);
        }

        OrderSequenceGenerator roundTripped;
        try (ObjectInputStream in = new ObjectInputStream(new ByteArrayInputStream(bytes.toByteArray()))) {
            roundTripped = (OrderSequenceGenerator) in.readObject();
        }

        assertSame(OrderSequenceGenerator.INSTANCE, roundTripped);
    }

    @Test
    void concurrentCallsNeverProduceDuplicateOrderNumbers() throws InterruptedException {
        int threadCount = 20;
        int callsPerThread = 50;
        Set<String> orderNumbers = ConcurrentHashMap.newKeySet();
        CountDownLatch ready = new CountDownLatch(threadCount);
        CountDownLatch go = new CountDownLatch(1);
        CountDownLatch done = new CountDownLatch(threadCount);
        ExecutorService pool = Executors.newFixedThreadPool(threadCount);

        for (int t = 0; t < threadCount; t++) {
            pool.execute(() -> {
                ready.countDown();
                await(go);
                for (int i = 0; i < callsPerThread; i++) {
                    orderNumbers.add(OrderSequenceGenerator.INSTANCE.nextOrderNumber());
                }
                done.countDown();
            });
        }

        await(ready);
        go.countDown();
        done.await();
        pool.shutdown();

        assertEquals(threadCount * callsPerThread, orderNumbers.size());
    }

    private static void await(CountDownLatch latch) {
        try {
            latch.await();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new RuntimeException(e);
        }
    }

    private static int numericPart(String orderNumber) {
        return Integer.parseInt(orderNumber.substring(orderNumber.indexOf('-') + 1));
    }
}
