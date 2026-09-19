package com.jk.explore.timeoutpattern;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

/** The two ways to call the supplier: wait for as long as it takes, or give up after a limit. */
public class Callers {

    private final ExecutorService pool;

    public Callers(ExecutorService pool) {
        this.pool = pool;
    }

    /** Starts the call on the pool, and returns the future for it. */
    public CompletableFuture<String> start(SupplierApi api, String sku) {
        return CompletableFuture.supplyAsync(() -> api.stockOf(sku), pool);
    }

    public String withTimeout(SupplierApi api, String sku, long millis) {
        CompletableFuture<String> call = start(api, sku);
        try {
            return call.get(millis, TimeUnit.MILLISECONDS);
        } catch (TimeoutException e) {
            call.cancel(true);
            return "stock unknown, try again shortly";
        } catch (InterruptedException | ExecutionException e) {
            throw new IllegalStateException(e);
        }
    }
}
