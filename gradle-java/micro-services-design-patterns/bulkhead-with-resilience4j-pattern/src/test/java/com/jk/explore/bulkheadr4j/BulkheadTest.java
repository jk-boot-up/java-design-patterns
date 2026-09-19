package com.jk.explore.bulkheadr4j;

import io.github.resilience4j.bulkhead.BulkheadFullException;
import org.junit.jupiter.api.Test;
import org.springframework.context.ConfigurableApplicationContext;

import java.util.List;
import java.util.concurrent.CompletableFuture;

import static com.jk.explore.bulkheadr4j.SupplierApplication.*;
import static org.junit.jupiter.api.Assertions.*;

class BulkheadTest {

    @Test
    void oneSharedCompartmentLetsTheFeedStarveCheckout() throws Exception {
        try (ConfigurableApplicationContext ctx = builder().run()) {
            SupplierService s = ctx.getBean(SupplierService.class);
            Gate gate = new Gate(4);
            List<Thread> jobs = hold(4, gate, s::sharedFeed);
            gate.awaitArrivals();
            assertThrows(BulkheadFullException.class, s::sharedCheckout);
            release(gate, jobs);
            assertEquals("sold", s.sharedCheckout());
        }
    }

    @Test
    void separateCompartmentsKeepCheckoutSelling() throws Exception {
        try (ConfigurableApplicationContext ctx = builder().run()) {
            SupplierService s = ctx.getBean(SupplierService.class);
            Gate gate = new Gate(2);
            List<Thread> jobs = hold(2, gate, s::feed);
            gate.awaitArrivals();
            assertThrows(BulkheadFullException.class, () -> s.feed(new Gate(1)));
            assertEquals("sold", s.checkout());
            assertEquals("feed batch skipped tonight", s.feedWithFallback(new Gate(1)));
            assertEquals(0, free(ctx, "feed"));
            assertEquals(4, free(ctx, "checkout"));
            release(gate, jobs);
            assertEquals(2, free(ctx, "feed"));
        }
    }

    @Test
    void aCallOnThisIsNotLimited() throws Exception {
        try (ConfigurableApplicationContext ctx = builder().run()) {
            SupplierService s = ctx.getBean(SupplierService.class);
            Gate gate = new Gate(10);
            List<Thread> jobs = hold(10, gate, s::feedThroughThis);
            gate.awaitArrivals();
            assertEquals(2, free(ctx, "feed"));
            release(gate, jobs);
        }
    }

    @Test
    void aThreadPoolCompartmentRunsTwoQueuesOneAndRefusesTheNext() throws Exception {
        try (ConfigurableApplicationContext ctx = builder().run()) {
            SupplierService s = ctx.getBean(SupplierService.class);
            Gate gate = new Gate(2);
            CompletableFuture<String> a = s.feedOnItsOwnThreads(gate);
            CompletableFuture<String> b = s.feedOnItsOwnThreads(gate);
            gate.awaitArrivals();
            CompletableFuture<String> queued = s.feedOnItsOwnThreads(gate);
            CompletableFuture<String> refused = s.feedOnItsOwnThreads(gate);
            assertEquals("BulkheadFullException", describe(refused));
            assertFalse(queued.isDone());
            gate.open();
            assertTrue(a.get().contains("bulkhead-feedpool"));
            assertNotNull(b.get());
            assertNotNull(queued.get());
        }
    }
}
