package com.jk.explore.futurepromisespring;

import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;

/** Six acts. Every wait is a latch or a gate, never a sleep. */
@SpringBootApplication
public class ProductPageApplication {

    public static void main(String[] args) throws Exception {
        System.out.println("FUTURE/PROMISE WITH SPRING — what @Async loses\n");
        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    static ConfigurableApplicationContext start(String... properties) {
        return new SpringApplicationBuilder(ProductPageApplication.class).properties(properties).run();
    }

    private static int maxInFlight(String... properties) throws Exception {
        try (ConfigurableApplicationContext context = start(properties)) {
            CatalogueLookups lookups = context.getBean(CatalogueLookups.class);
            Flight flight = context.getBean(Flight.class);
            Gate gate = new Gate();
            flight.reset(gate);
            CompletableFuture<String> price = lookups.price("ESP-001");
            CompletableFuture<String> stock = lookups.stock("ESP-001");
            CompletableFuture<String> rating = lookups.rating("ESP-001");
            long deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(2);
            while (flight.inFlightNow() < 3 && System.nanoTime() < deadline) {
                Thread.onSpinWait();
            }
            gate.open();
            CompletableFuture.allOf(price, stock, rating).get(10, TimeUnit.SECONDS);
            return flight.maxInFlight();
        }
    }

    private static void actOne() throws Exception {
        System.out.println("ONE. @Async returns a future, and the pool decides how concurrent it is.");
        System.out.println("  three independent lookups, price, stock and rating, submitted at once.");
        System.out.println("  on the default pool, lookups in flight at the same moment: " + maxInFlight());
        System.out.println("  on a pool of one thread: " + maxInFlight("spring.task.execution.pool.core-size=1",
                "spring.task.execution.pool.max-size=1", "spring.task.execution.pool.queue-capacity=10"));
        System.out.println("  the annotation asked for concurrency. the pool decided whether to give it.\n");
    }

    private static void actTwo() throws Exception {
        System.out.println("TWO. Exceptions: a future carries them, a void method loses them.");
        try (ConfigurableApplicationContext context = start()) {
            CatalogueLookups lookups = context.getBean(CatalogueLookups.class);
            try {
                lookups.failingRating("ESP-001").join();
            } catch (CompletionException e) {
                System.out.println("  a method returning a future: the caller sees " + e.getClass().getSimpleName()
                        + ", cause \"" + e.getCause().getMessage() + "\".");
                StackTraceElement top = e.getCause().getStackTrace()[0];
                boolean callerAppears = false;
                for (StackTraceElement frame : e.getCause().getStackTrace()) {
                    callerAppears |= frame.getMethodName().equals("actTwo");
                }
                System.out.println("  the calling method appears in that stack trace: " + callerAppears + ". the trace belongs to a pool thread.");
            }
            lookups.notifyWarehouse("ESP-001");
            @SuppressWarnings("unchecked")
            List<String> uncaught = (List<String>) context.getBean("uncaughtAsyncExceptions");
            long deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(5);
            while (uncaught.isEmpty() && System.nanoTime() < deadline) {
                Thread.onSpinWait();
            }
            System.out.println("  a void method threw, and the caller got: nothing. the call returned normally.");
            System.out.println("  the only place it went is a handler you have to register: " + uncaught + "\n");
        }
    }

    private static void actThree() throws Exception {
        System.out.println("THREE. Thread-locals do not cross the thread boundary.");
        try (ConfigurableApplicationContext context = start()) {
            CustomerContext.set(7);
            String seen = context.getBean(CatalogueLookups.class).whoseOrderIsThis().get(5, TimeUnit.SECONDS);
            System.out.println("  the caller is working for customer 7. the async method asked whose order it is: \"" + seen + "\".");
            System.out.println("  request context, security context and logging context are all thread-locals, and are all gone.");
            CustomerContext.clear();
        }
        try (ConfigurableApplicationContext context = start("demo.propagate-context=true")) {
            CustomerContext.set(7);
            String seen = context.getBean(CatalogueLookups.class).whoseOrderIsThis().get(5, TimeUnit.SECONDS);
            System.out.println("  with a TaskDecorator that copies it across: \"" + seen + "\". the fix is a bean, and it is yours to write.\n");
            CustomerContext.clear();
        }
    }

    private static void actFour() throws Exception {
        System.out.println("FOUR. A timeout is the caller giving up. The work does not stop.");
        try (ConfigurableApplicationContext context = start()) {
            CatalogueLookups lookups = context.getBean(CatalogueLookups.class);
            CountDownLatch started = new CountDownLatch(1);
            Gate gate = new Gate();
            AtomicBoolean finished = new AtomicBoolean();
            CompletableFuture<String> slow = lookups.slowLookup(started, gate, finished);
            started.await(10, TimeUnit.SECONDS);
            try {
                slow.orTimeout(200, TimeUnit.MILLISECONDS).join();
            } catch (CompletionException e) {
                System.out.println("  the caller waited 200ms and got: " + e.getCause().getClass().getSimpleName() + ".");
            }
            System.out.println("  the task had finished when the caller gave up: " + finished.get() + ".");
            gate.open();
            long deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(5);
            while (!finished.get() && System.nanoTime() < deadline) {
                Thread.onSpinWait();
            }
            System.out.println("  and then it ran to the end anyway, and did its work: " + finished.get() + ". nobody was waiting for the answer.\n");
        }
    }

    private static void actFive() throws Exception {
        System.out.println("FIVE. cancel(true) on a CompletableFuture interrupts nothing.");
        try (ConfigurableApplicationContext context = start()) {
            CatalogueLookups lookups = context.getBean(CatalogueLookups.class);
            CountDownLatch started = new CountDownLatch(1);
            Gate gate = new Gate();
            AtomicBoolean finished = new AtomicBoolean();
            CompletableFuture<String> slow = lookups.slowLookup(started, gate, finished);
            started.await(10, TimeUnit.SECONDS);
            boolean cancelled = slow.cancel(true);
            System.out.println("  cancel(true) reported: " + cancelled + ". isCancelled: " + slow.isCancelled() + ".");
            gate.open();
            long deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(5);
            while (!finished.get() && System.nanoTime() < deadline) {
                Thread.onSpinWait();
            }
            System.out.println("  the task ran to completion anyway: " + finished.get() + ". the flag was set on the future, and the thread was never told.\n");
        }
    }

    private static void actSix() throws Exception {
        System.out.println("SIX. Composing the page, and one lookup failing.");
        try (ConfigurableApplicationContext context = start()) {
            CatalogueLookups lookups = context.getBean(CatalogueLookups.class);
            String page = lookups.price("ESP-001").thenCombine(lookups.stock("ESP-001"), (p, s) -> p + ", " + s)
                    .thenCombine(lookups.rating("ESP-001"), (ps, r) -> ps + ", " + r).get(5, TimeUnit.SECONDS);
            System.out.println("  assembled from three futures, with no get() until the end: " + page);
            String fallback = lookups.price("ESP-001").thenCombine(lookups.stock("ESP-001"), (p, s) -> p + ", " + s)
                    .thenCombine(lookups.failingRating("ESP-001").exceptionally(t -> "rating unavailable"), (ps, r) -> ps + ", " + r)
                    .get(5, TimeUnit.SECONDS);
            System.out.println("  with the review service down and a fallback chosen at that one step: " + fallback);
            System.out.println("  without the fallback, one failing lookup fails the whole page.");
            System.out.println("  verdict: return a CompletableFuture, never void; propagate context on purpose; and treat a timeout as giving up, not stopping.");
            System.out.println("  where you have met this: every @Async method that returns a CompletableFuture.");
        }
    }
}
