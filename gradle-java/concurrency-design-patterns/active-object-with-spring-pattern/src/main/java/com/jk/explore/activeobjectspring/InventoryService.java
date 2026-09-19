package com.jk.explore.activeobjectspring;

import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * <strong>An active object that is a bean.</strong> {@code stock} is a plain field: no lock, not volatile.
 * It is safe only because every change runs on the one {@code inventory-} thread, and that is true only
 * for calls that go through Spring's proxy.
 */
@Service
public class InventoryService {

    private int stock;
    private final AtomicInteger processed = new AtomicInteger();

    @Async("inventoryExecutor")
    public CompletableFuture<Integer> restock(int amount) {
        stock += amount;
        processed.incrementAndGet();
        return CompletableFuture.completedFuture(stock);
    }

    @Async("inventoryExecutor")
    public CompletableFuture<Integer> restockWithWork(int amount, long spinNanos) {
        long until = System.nanoTime() + spinNanos;
        while (System.nanoTime() < until) {
            Thread.onSpinWait();
        }
        return restock(amount);
    }

    /** Reads the stock, holds at a gate, then writes what it read plus the amount: a change in two steps. */
    @Async("inventoryExecutor")
    public CompletableFuture<Integer> slowRestock(int amount, CountDownLatch holdingTheOldValue, Gate gate) {
        int seen = stock;
        holdingTheOldValue.countDown();
        gate.awaitOpen();
        stock = seen + amount;
        return CompletableFuture.completedFuture(stock);
    }

    /** Calls {@link #restock} through {@code this}: no proxy, so it runs here, on the caller's thread. */
    public int restockThroughThis(int amount) {
        return unwrap(restock(amount));
    }

    @Async("inventoryExecutor")
    public CompletableFuture<Integer> failWith(String reason) {
        throw new IllegalStateException(reason + " [raised on " + Thread.currentThread().getName() + "]");
    }

    @Async("inventoryExecutor")
    public CompletableFuture<Integer> available() {
        return CompletableFuture.completedFuture(stock);
    }

    /** A read that skips the mailbox: it runs on the caller's thread, and sees whatever the field holds right now. */
    public int peekStock() {
        return stock;
    }

    public int processed() {
        return processed.get();
    }

    private static int unwrap(CompletableFuture<Integer> done) {
        return done.join();
    }
}
