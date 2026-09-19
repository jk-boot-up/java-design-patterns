package com.jk.explore.futurepromise;

import com.jk.explore.futurepromise.domain.Lookup;
import com.jk.explore.futurepromise.domain.ProductPageView;
import com.jk.explore.futurepromise.harness.Gate;
import com.jk.explore.futurepromise.naive.SequentialProductPage;
import com.jk.explore.futurepromise.pattern.AsyncFailure;
import com.jk.explore.futurepromise.pattern.CooperativeCancellation;
import com.jk.explore.futurepromise.pattern.ConcurrentProductPage;
import com.jk.explore.futurepromise.pattern.FutureAndPromise;
import com.jk.explore.futurepromise.pattern.UnboundedWait;

import java.math.BigDecimal;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

/**
 * Six acts. The only deliberate delay anywhere in this class is
 * {@link #LOOKUP_MILLIS} — the named, measured subject the whole video is
 * about — plus the rescue timeout in act five, which is the demonstration's
 * own escape hatch from a genuine hang, not a wait for anything to finish.
 */
public final class ProductPageDemo {

    /** How long one catalogue lookup takes. Named and printed, never hidden. */
    private static final long LOOKUP_MILLIS = 200;

    private static final String SKU = "ESP-001";

    private static final Lookup<BigDecimal> PRICE = sku -> {
        sleep();
        return new BigDecimal("129.99");
    };
    private static final Lookup<Integer> STOCK = sku -> {
        sleep();
        return 7;
    };
    private static final Lookup<Double> RATING = sku -> {
        sleep();
        return 4.6;
    };

    private static void sleep() {
        try {
            Thread.sleep(LOOKUP_MILLIS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    public static void main(String[] args) throws Exception {
        System.out.println("FUTURE/PROMISE — the answer you do not have yet\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    private static void actOne() {
        System.out.println("ONE. Sequential — price, then stock, then rating.");
        SequentialProductPage page = new SequentialProductPage(PRICE, STOCK, RATING);
        ProductPageView view = page.render(SKU);
        System.out.printf("  price £%s, stock %d, rating %.1f%n", view.price(), view.stock(), view.rating());
        System.out.printf("  rendered in %.0fms — three lookups, none depending on the others,%n",
                view.elapsedNanos() / 1_000_000.0);
        System.out.println("  paid for one after another anyway.");
        System.out.println();
    }

    private static void actTwo() throws ExecutionException, InterruptedException {
        System.out.println("TWO. Concurrent — all three submitted at once.");
        ExecutorService pool = Executors.newFixedThreadPool(3);
        try {
            ConcurrentProductPage page = new ConcurrentProductPage(PRICE, STOCK, RATING, pool);
            ProductPageView view = page.render(SKU);
            System.out.printf("  price £%s, stock %d, rating %.1f%n", view.price(), view.stock(), view.rating());
            System.out.printf("  rendered in %.0fms — roughly one lookup's cost, not three.%n",
                    view.elapsedNanos() / 1_000_000.0);
        } finally {
            pool.shutdown();
            pool.awaitTermination(2, TimeUnit.SECONDS);
        }
        System.out.println();
    }

    private static void actThree() {
        System.out.println("THREE. Future and Promise — the two halves, made explicit.");
        String result = FutureAndPromise.handOff(() -> {
            sleep();
            return "£129.99";
        });
        System.out.println("  the writer thread completed the promise: " + result);
        System.out.println("  the reader thread was blocked on the future until it did.");
        System.out.println();
    }

    private static void actFour() {
        System.out.println("FOUR. Exceptions move — surfacing wrapped, on get().");
        ExecutorService pool = Executors.newSingleThreadExecutor();
        try {
            AsyncFailure.Outcome outcome = AsyncFailure.attempt(pool,
                    () -> { throw new IllegalStateException("catalogue unavailable for " + SKU); });
            System.out.println("  cause: " + outcome.causeMessage());
            System.out.println("  stack top: " + outcome.stackTop());
            System.out.println("  the call site that submitted this task appears nowhere above: "
                    + outcome.traceOmits("actFour"));
        } finally {
            pool.shutdown();
        }
        System.out.println();
    }

    private static void actFive() {
        System.out.println("FIVE. get() with no timeout is a hang.");
        ExecutorService pool = Executors.newSingleThreadExecutor();
        try {
            UnboundedWait.Outcome outcome = UnboundedWait.attemptGet(pool, new Gate(), 200);
            System.out.println("  a task parked forever, waited on with a 200ms rescue timeout:");
            System.out.println("  timed out: " + outcome.timedOut() + ", after " + outcome.waitedMillis() + "ms");
            System.out.println("  a bare get() with no timeout does not time out — it just never returns.");
        } finally {
            pool.shutdown();
        }
        System.out.println();
    }

    private static void actSix() {
        System.out.println("SIX. Cancellation is cooperative, and may do nothing.");
        ExecutorService pool = Executors.newSingleThreadExecutor();
        try {
            CooperativeCancellation.Outcome outcome = CooperativeCancellation.attempt(pool);
            System.out.println("  cancel(true) reported: " + outcome.reportedCancelled());
            System.out.println("  the task ran to completion anyway: " + outcome.taskRanToCompletion());
            System.out.println("  it caught every interrupt and carried on — cancel asked; the task said no.");
        } finally {
            pool.shutdown();
        }
    }
}
