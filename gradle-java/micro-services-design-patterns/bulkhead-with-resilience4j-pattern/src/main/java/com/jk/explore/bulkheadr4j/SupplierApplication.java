package com.jk.explore.bulkheadr4j;

import io.github.resilience4j.bulkhead.BulkheadFullException;
import io.github.resilience4j.bulkhead.BulkheadRegistry;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.function.Consumer;

@SpringBootApplication
public class SupplierApplication {

    static SpringApplicationBuilder builder() {
        return new SpringApplicationBuilder(SupplierApplication.class).web(WebApplicationType.NONE);
    }

    static int free(ConfigurableApplicationContext ctx, String name) {
        return ctx.getBean(BulkheadRegistry.class).bulkhead(name).getMetrics().getAvailableConcurrentCalls();
    }

    /** Starts {@code count} threads that each make one call and stop at the gate. */
    static List<Thread> hold(int count, Gate gate, Consumer<Gate> call) {
        List<Thread> threads = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            Thread thread = new Thread(() -> call.accept(gate), "feed-" + i);
            thread.start();
            threads.add(thread);
        }
        return threads;
    }

    static String describe(CompletableFuture<String> future) {
        try {
            future.get();
            return "no";
        } catch (ExecutionException e) {
            return e.getCause().getClass().getSimpleName();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return "interrupted";
        }
    }

    static void release(Gate gate, List<Thread> threads) throws InterruptedException {
        gate.open();
        for (Thread thread : threads) {
            thread.join();
        }
    }

    public static void main(String[] args) throws Exception {
        try (ConfigurableApplicationContext ctx = builder().run()) {
            SupplierService service = ctx.getBean(SupplierService.class);

            System.out.println("ONE. One compartment for everything.");
            Gate slow = new Gate(4);
            List<Thread> feedJobs = hold(4, slow, service::sharedFeed);
            slow.awaitArrivals();
            try {
                service.sharedCheckout();
            } catch (BulkheadFullException e) {
                System.out.println("  four slow feed jobs hold every permit. checkout is refused: " + e.getClass().getSimpleName() + ".");
            }
            release(slow, feedJobs);
            System.out.println("  a background job stopped the shop selling.");

            System.out.println("TWO. A compartment each.");
            Gate two = new Gate(2);
            feedJobs = hold(2, two, service::feed);
            two.awaitArrivals();
            try {
                service.feed(new Gate(1));
            } catch (BulkheadFullException e) {
                System.out.println("  a third feed job is refused: " + e.getClass().getSimpleName() + ".");
            }
            System.out.println("  checkout while two feed jobs are stuck: " + service.checkout() + ".");

            System.out.println("THREE. What a full compartment does to its callers.");
            System.out.println("  with a fallback method, the third feed job gets: " + service.feedWithFallback(new Gate(1)) + ".");

            System.out.println("FOUR. The cost of the wall.");
            System.out.println("  permits free in the feed compartment: " + free(ctx, "feed") + ". in the checkout compartment: " + free(ctx, "checkout") + ".");
            System.out.println("  checkout's four permits cannot help the feed, even now.");
            release(two, feedJobs);

            System.out.println("FIVE. The annotation is a proxy.");
            Gate ten = new Gate(10);
            feedJobs = hold(10, ten, service::feedThroughThis);
            ten.awaitArrivals();
            System.out.println("  10 feed jobs called through this, in a compartment of 2. all 10 are inside at once.");
            System.out.println("  permits free in the feed compartment: " + free(ctx, "feed") + ". it never saw them.");
            release(ten, feedJobs);

            System.out.println("SIX. A compartment with its own threads.");
            Gate pool = new Gate(2);
            CompletableFuture<String> first = service.feedOnItsOwnThreads(pool);
            CompletableFuture<String> second = service.feedOnItsOwnThreads(pool);
            pool.awaitArrivals();
            CompletableFuture<String> queued = service.feedOnItsOwnThreads(pool);
            CompletableFuture<String> refused = service.feedOnItsOwnThreads(pool);
            System.out.println("  four submissions, and the caller was never blocked. running: 2. waiting in the queue: 1.");
            System.out.println("  the fourth was refused: " + describe(refused) + ".");
            pool.open();
            System.out.println("  the first ran on: " + first.get().substring("feed batch done on ".length()).replaceAll("-\\d+$", "-N") + ". all three finished: "
                    + (second.get() != null && queued.get() != null) + ".");
        }
    }
}
