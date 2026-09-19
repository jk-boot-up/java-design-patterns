package com.jk.explore.scattergather;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

/** Sends one question to every supplier at once, and gathers whatever answers arrive before the deadline. */
public class ScatterGather {

    public record Result(List<Quote> quotes, List<String> missing) {

        public Quote best() {
            return quotes.stream().min(java.util.Comparator.comparingLong(Quote::pence)).orElse(null);
        }
    }

    private final ExecutorService pool;

    public ScatterGather(ExecutorService pool) {
        this.pool = pool;
    }

    public Result ask(List<Supplier> suppliers, String sku, long deadlineMillis) {
        List<CompletableFuture<Quote>> scattered = new ArrayList<>();
        for (Supplier s : suppliers) {
            scattered.add(CompletableFuture.supplyAsync(() -> s.quote(sku), pool));
        }
        long deadline = System.nanoTime() + TimeUnit.MILLISECONDS.toNanos(deadlineMillis);
        List<Quote> quotes = new ArrayList<>();
        List<String> missing = new ArrayList<>();
        for (int i = 0; i < suppliers.size(); i++) {
            long left = Math.max(0, deadline - System.nanoTime());
            try {
                quotes.add(scattered.get(i).get(left, TimeUnit.NANOSECONDS));
            } catch (TimeoutException e) {
                missing.add(suppliers.get(i).name() + " (too slow)");
            } catch (ExecutionException e) {
                missing.add(suppliers.get(i).name() + " (" + e.getCause().getMessage() + ")");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                missing.add(suppliers.get(i).name() + " (interrupted)");
            }
        }
        return new Result(quotes, missing);
    }
}
