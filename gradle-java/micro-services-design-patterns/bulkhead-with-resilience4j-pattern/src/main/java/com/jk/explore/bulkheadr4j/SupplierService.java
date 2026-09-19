package com.jk.explore.bulkheadr4j;

import io.github.resilience4j.bulkhead.annotation.Bulkhead;
import org.springframework.stereotype.Service;

import java.util.concurrent.CompletableFuture;

/**
 * The supplier feed and checkout, each behind a bulkhead. The gate stands in for a partner API
 * that is very slow: a call that has entered holds its place until the gate opens.
 */
@Service
public class SupplierService {

    @Bulkhead(name = "shared")
    public String sharedFeed(Gate gate) {
        gate.arriveAndWait();
        return "feed batch done";
    }

    @Bulkhead(name = "shared")
    public String sharedCheckout() {
        return "sold";
    }

    @Bulkhead(name = "feed")
    public String feed(Gate gate) {
        gate.arriveAndWait();
        return "feed batch done";
    }

    @Bulkhead(name = "feed", fallbackMethod = "skipTonight")
    public String feedWithFallback(Gate gate) {
        gate.arriveAndWait();
        return "feed batch done";
    }

    String skipTonight(Gate gate, Throwable cause) {
        return "feed batch skipped tonight";
    }

    @Bulkhead(name = "checkout")
    public String checkout() {
        return "sold";
    }

    /** A call on this: the proxy, and its bulkhead, never see it. */
    public String feedThroughThis(Gate gate) {
        return this.feed(gate);
    }

    @Bulkhead(name = "feedpool", type = Bulkhead.Type.THREADPOOL)
    public CompletableFuture<String> feedOnItsOwnThreads(Gate gate) {
        gate.arriveAndWait();
        return CompletableFuture.completedFuture("feed batch done on " + Thread.currentThread().getName());
    }
}
