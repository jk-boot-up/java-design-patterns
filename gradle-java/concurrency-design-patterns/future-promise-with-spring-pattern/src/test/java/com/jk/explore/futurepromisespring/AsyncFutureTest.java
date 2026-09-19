package com.jk.explore.futurepromisespring;

import org.junit.jupiter.api.Test;
import org.springframework.context.ConfigurableApplicationContext;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** Every wait is a latch, a gate or a bounded spin. No test sleeps. */
class AsyncFutureTest {

    private static int peak(String... properties) throws Exception {
        try (ConfigurableApplicationContext context = ProductPageApplication.start(properties)) {
            CatalogueLookups lookups = context.getBean(CatalogueLookups.class);
            Flight flight = context.getBean(Flight.class);
            Gate gate = new Gate();
            flight.reset(gate);
            CompletableFuture<String> a = lookups.price("x");
            CompletableFuture<String> b = lookups.stock("x");
            CompletableFuture<String> c = lookups.rating("x");
            long deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(2);
            while (flight.inFlightNow() < 3 && System.nanoTime() < deadline) {
                Thread.onSpinWait();
            }
            gate.open();
            CompletableFuture.allOf(a, b, c).get(10, TimeUnit.SECONDS);
            return flight.maxInFlight();
        }
    }

    @Test
    void theDefaultPoolRunsAllThreeLookupsAtOnceAndAPoolOfOneRunsOneAtATime() throws Exception {
        assertEquals(3, peak());
        assertEquals(1, peak("spring.task.execution.pool.core-size=1", "spring.task.execution.pool.max-size=1",
                "spring.task.execution.pool.queue-capacity=10"));
    }

    @Test
    void aFutureCarriesTheExceptionAndItsTraceBelongsToThePoolThread() {
        try (ConfigurableApplicationContext context = ProductPageApplication.start()) {
            CompletionException e = assertThrows(CompletionException.class,
                    () -> context.getBean(CatalogueLookups.class).failingRating("x").join());
            assertEquals("the review service is down", e.getCause().getMessage());
            for (StackTraceElement frame : e.getCause().getStackTrace()) {
                assertFalse(frame.getClassName().contains("AsyncFutureTest"), "the calling test must not appear: " + frame);
            }
        }
    }

    @Test
    void aVoidMethodsExceptionReachesOnlyTheHandlerYouRegistered() {
        try (ConfigurableApplicationContext context = ProductPageApplication.start()) {
            @SuppressWarnings("unchecked")
            List<String> uncaught = (List<String>) context.getBean("uncaughtAsyncExceptions");
            context.getBean(CatalogueLookups.class).notifyWarehouse("ESP-001");
            long deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(5);
            while (uncaught.isEmpty() && System.nanoTime() < deadline) {
                Thread.onSpinWait();
            }
            assertEquals(List.of("notifyWarehouse: the warehouse feed rejected ESP-001"), uncaught);
        }
    }

    @Test
    void aThreadLocalDoesNotCrossToThePoolUnlessATaskDecoratorCopiesIt() throws Exception {
        try (ConfigurableApplicationContext context = ProductPageApplication.start()) {
            CustomerContext.set(7);
            assertEquals("customer null", context.getBean(CatalogueLookups.class).whoseOrderIsThis().get(5, TimeUnit.SECONDS));
            CustomerContext.clear();
        }
        try (ConfigurableApplicationContext context = ProductPageApplication.start("demo.propagate-context=true")) {
            CustomerContext.set(7);
            assertEquals("customer 7", context.getBean(CatalogueLookups.class).whoseOrderIsThis().get(5, TimeUnit.SECONDS));
            CustomerContext.clear();
        }
    }

    @Test
    void aTimeoutStopsTheCallerWaitingButTheTaskStillRunsToTheEnd() throws Exception {
        try (ConfigurableApplicationContext context = ProductPageApplication.start()) {
            CountDownLatch started = new CountDownLatch(1);
            Gate gate = new Gate();
            AtomicBoolean finished = new AtomicBoolean();
            CompletableFuture<String> slow = context.getBean(CatalogueLookups.class).slowLookup(started, gate, finished);
            assertTrue(started.await(10, TimeUnit.SECONDS));
            CompletionException e = assertThrows(CompletionException.class, () -> slow.orTimeout(200, TimeUnit.MILLISECONDS).join());
            assertEquals("TimeoutException", e.getCause().getClass().getSimpleName());
            assertFalse(finished.get());
            gate.open();
            long deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(5);
            while (!finished.get() && System.nanoTime() < deadline) {
                Thread.onSpinWait();
            }
            assertTrue(finished.get());
        }
    }

    @Test
    void cancelTrueOnACompletableFutureInterruptsNothing() throws Exception {
        try (ConfigurableApplicationContext context = ProductPageApplication.start()) {
            CountDownLatch started = new CountDownLatch(1);
            Gate gate = new Gate();
            AtomicBoolean finished = new AtomicBoolean();
            CompletableFuture<String> slow = context.getBean(CatalogueLookups.class).slowLookup(started, gate, finished);
            assertTrue(started.await(10, TimeUnit.SECONDS));
            assertTrue(slow.cancel(true));
            assertTrue(slow.isCancelled());
            gate.open();
            long deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(5);
            while (!finished.get() && System.nanoTime() < deadline) {
                Thread.onSpinWait();
            }
            assertTrue(finished.get(), "the thread was never told");
        }
    }

    @Test
    void combiningFuturesNeedsAFallbackAtTheStepThatCanFail() throws Exception {
        try (ConfigurableApplicationContext context = ProductPageApplication.start()) {
            CatalogueLookups l = context.getBean(CatalogueLookups.class);
            assertEquals("price £129.99, rating unavailable",
                    l.price("x").thenCombine(l.failingRating("x").exceptionally(t -> "rating unavailable"), (p, r) -> p + ", " + r).get(5, TimeUnit.SECONDS));
            CompletionException e = assertThrows(CompletionException.class,
                    () -> l.price("x").thenCombine(l.failingRating("x"), (p, r) -> p + r).join());
            assertEquals("the review service is down", e.getCause().getMessage());
        }
    }
}
