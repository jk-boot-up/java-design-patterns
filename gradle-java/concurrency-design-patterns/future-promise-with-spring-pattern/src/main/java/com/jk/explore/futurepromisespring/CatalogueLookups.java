package com.jk.explore.futurepromisespring;

import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * <strong>Three independent lookups, each on the pool.</strong> The partner project, Future/Promise,
 * built the handoff by hand. Here {@code @Async} returns a {@code CompletableFuture}, and the container
 * completes it.
 */
@Service
public class CatalogueLookups {

    private final Flight flight;

    public CatalogueLookups(Flight flight) {
        this.flight = flight;
    }

    @Async
    public CompletableFuture<String> price(String sku) {
        return lookup("price £129.99");
    }

    @Async
    public CompletableFuture<String> stock(String sku) {
        return lookup("stock 7");
    }

    @Async
    public CompletableFuture<String> rating(String sku) {
        return lookup("rating 4.6");
    }

    @Async
    public CompletableFuture<String> failingRating(String sku) {
        throw new IllegalStateException("the review service is down");
    }

    private CompletableFuture<String> lookup(String answer) {
        flight.begin();
        try {
            return CompletableFuture.completedFuture(answer);
        } finally {
            flight.end();
        }
    }

    /** A void method: nobody can ask it for its exception. */
    @Async
    public void notifyWarehouse(String sku) {
        throw new IllegalStateException("the warehouse feed rejected " + sku);
    }

    /** Which customer this thread thinks it is working for, read on whatever thread runs the method. */
    @Async
    public CompletableFuture<String> whoseOrderIsThis() {
        return CompletableFuture.completedFuture("customer " + CustomerContext.get());
    }

    /** A slow task that records whether it ran to the end, whatever the caller did in the meantime. */
    @Async
    public CompletableFuture<String> slowLookup(CountDownLatch started, Gate gate, AtomicBoolean finished) {
        started.countDown();
        gate.awaitOpen();
        finished.set(true);
        return CompletableFuture.completedFuture("late answer");
    }
}
