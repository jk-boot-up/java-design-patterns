package com.jk.explore.threadpoolspring;

import org.springframework.context.annotation.Lazy;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

/**
 * <strong>Packing an order, on a pool the container owns.</strong> The partner project,
 * Thread Pool, built {@code BoundedPackingPool} by hand around a {@code ThreadPoolExecutor}. Here one
 * annotation sends the method to Spring's executor, and the pool's shape is configuration.
 */
@Service
public class PackingService {

    private final PackingService self;

    public PackingService(@Lazy PackingService self) {
        this.self = self;
    }

    /** Runs on the pool: the thread that runs it is not the thread that called it. */
    @Async
    public CompletableFuture<String> pack(int orderId, CountDownLatch started, Gate gate) {
        started.countDown();
        gate.awaitOpen();
        return CompletableFuture.completedFuture(Thread.currentThread().getName());
    }

    /** Calls {@link #pack} through {@code this}, which skips the proxy, so the annotation is never seen. */
    public CompletableFuture<String> packThroughThis(int orderId) {
        return pack(orderId, new CountDownLatch(1), openGate());
    }

    /** An outer task that waits for an inner one on the same pool. With one thread it can never finish. */
    @Async
    public CompletableFuture<String> packAndWaitForALabel() {
        try {
            return CompletableFuture.completedFuture(self.printLabel().get(300, TimeUnit.MILLISECONDS));
        } catch (TimeoutException e) {
            return CompletableFuture.completedFuture("starved: the label task never got a thread");
        } catch (Exception e) {
            throw new IllegalStateException(e);
        }
    }

    @Async
    public CompletableFuture<String> printLabel() {
        return CompletableFuture.completedFuture("label printed");
    }

    private static Gate openGate() {
        Gate g = new Gate();
        g.open();
        return g;
    }
}
