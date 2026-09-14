package com.jk.explore.bulkhead;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

/**
 * Four acts. The supplier feed is stuck on a slow partner in every one of them; what
 * changes is whether checkout can still get a thread.
 *
 * This is the only project in the category that uses real threads, so it is also the
 * only one whose timings are real. They are printed rounded, because the shape is the
 * lesson and the digits wobble.
 */
public final class BulkheadDemo {

    /** How long a shopper is prepared to wait before the sale is lost. */
    private static final long SHOPPER_PATIENCE_MILLIS = 300;

    public static void main(String[] args) throws Exception {
        System.out.println("Bulkhead: a slow supplier feed and a checkout that must not wait");
        System.out.println();

        oneSharedPool();
        twoBulkheads();
        aFullBulkheadRefusesQuickly();
        theCostOfPartitioning();
    }

    /** Act 1: everything shares four threads, and the shop stops selling. */
    private static void oneSharedPool() throws Exception {
        JobLog log = new JobLog();
        Gate partnerApi = new Gate();

        try (Bulkhead shared = new Bulkhead("shared", 4, 4, log)) {
            SupplierFeed feed = new SupplierFeed(partnerApi);
            for (int i = 1; i <= 4; i++) {
                shared.submit("feed-" + i, feed.importBatch(i));
            }
            waitUntilBusy(shared, 4);

            Future<String> sale = shared.submit("checkout", new Checkout().takePayment("ORD-5001"));
            String outcome = waitFor(sale);

            System.out.println("1. One shared pool of four threads");
            System.out.print(log.timeline());
            System.out.println("  checkout: " + outcome);
            System.out.println("  note what is missing from that timeline: checkout. It has no line");
            System.out.println("  because it never started.");
            System.out.printf("  all %d threads are held by the feed, and the sale is lost --%n",
                    shared.size());
            System.out.println("  the shop stopped selling because of a background job.");
            partnerApi.open();
            System.out.println();
        }
    }

    /** Act 2: two pots of threads, and checkout never notices. */
    private static void twoBulkheads() throws Exception {
        JobLog log = new JobLog();
        Gate partnerApi = new Gate();

        try (Bulkhead feedPool = new Bulkhead("feed", 2, 2, log);
             Bulkhead checkoutPool = new Bulkhead("checkout", 2, 2, log)) {

            SupplierFeed feed = new SupplierFeed(partnerApi);
            for (int i = 1; i <= 4; i++) {
                feedPool.submit("feed-" + i, feed.importBatch(i));
            }
            waitUntilBusy(feedPool, 2);

            Future<String> sale = checkoutPool.submit("checkout",
                    new Checkout().takePayment("ORD-5001"));
            String outcome = waitFor(sale);

            System.out.println("2. Two bulkheads: the feed has its own threads");
            System.out.print(log.timeline());
            System.out.println("  checkout: " + outcome);
            System.out.printf("  the feed is jammed -- %d threads busy, %d jobs queued --%n",
                    feedPool.busyThreads(), feedPool.queued());
            System.out.println("  and the shop is still selling, because it never shared.");
            partnerApi.open();
            System.out.println();
        }
    }

    /** Act 3: a full bulkhead says no, straight away. */
    private static void aFullBulkheadRefusesQuickly() {
        JobLog log = new JobLog();
        Gate partnerApi = new Gate();

        try (Bulkhead feedPool = new Bulkhead("feed", 2, 2, log)) {
            SupplierFeed feed = new SupplierFeed(partnerApi);
            for (int i = 1; i <= 4; i++) {
                feedPool.submit("feed-" + i, feed.importBatch(i));
            }
            waitUntilBusy(feedPool, 2);

            String outcome;
            long startedAt = System.currentTimeMillis();
            try {
                feedPool.submit("feed-5", feed.importBatch(5));
                outcome = "accepted, which it should not have been";
            } catch (BulkheadFullException full) {
                outcome = full.getMessage() + " (in "
                        + (System.currentTimeMillis() - startedAt) + "ms)";
            }

            System.out.println("3. A fifth batch arrives with nowhere to go");
            System.out.println("  " + outcome);
            System.out.printf("  %d accepted, %d refused%n", feedPool.accepted(), feedPool.rejected());
            System.out.println("  an unbounded queue would have taken it, and every batch after it,");
            System.out.println("  until the shop ran out of memory instead of out of threads.");
            partnerApi.open();
            System.out.println();
        }
    }

    /** Act 4: the honest price. */
    private static void theCostOfPartitioning() throws Exception {
        JobLog log = new JobLog();
        Gate partnerApi = new Gate();

        try (Bulkhead feedPool = new Bulkhead("feed", 2, 2, log);
             Bulkhead checkoutPool = new Bulkhead("checkout", 2, 2, log)) {

            SupplierFeed feed = new SupplierFeed(partnerApi);
            for (int i = 1; i <= 4; i++) {
                feedPool.submit("feed-" + i, feed.importBatch(i));
            }
            waitUntilBusy(feedPool, 2);

            System.out.println("4. What the partition costs on a quiet afternoon");
            System.out.printf("  feed:     %d threads, %d busy, %d queued and waiting%n",
                    feedPool.size(), feedPool.busyThreads(), feedPool.queued());
            System.out.printf("  checkout: %d threads, %d busy, %d idle%n",
                    checkoutPool.size(), checkoutPool.busyThreads(), checkoutPool.idleThreads());
            System.out.println("  two threads are doing nothing while two jobs wait for a thread.");
            System.out.println("  One shared pool would have finished the feed sooner. Bulkheads buy");
            System.out.println("  isolation and they pay for it in throughput -- that is the trade,");
            System.out.println("  and it is worth making for anything that must never be starved.");

            partnerApi.open();
            List<Future<String>> finished = new ArrayList<>();
            finished.add(checkoutPool.submit("checkout", new Checkout().takePayment("ORD-5002")));
            for (Future<String> f : finished) {
                f.get(5, TimeUnit.SECONDS);
            }
        }
    }

    /** Waits for a job, giving up when a shopper would. */
    private static String waitFor(Future<String> sale) throws InterruptedException, ExecutionException {
        try {
            return sale.get(SHOPPER_PATIENCE_MILLIS, TimeUnit.MILLISECONDS);
        } catch (TimeoutException e) {
            return "still waiting for a thread after " + SHOPPER_PATIENCE_MILLIS + "ms";
        }
    }

    /**
     * Waits until the bulkhead's threads have actually picked up their work.
     *
     * Submitting a job and having it start are two different moments, and the demo
     * needs the second one. Spinning on the count is not elegant, but it is honest:
     * it waits exactly as long as necessary and no longer.
     */
    private static void waitUntilBusy(Bulkhead bulkhead, int threads) {
        long giveUpAt = System.currentTimeMillis() + 5_000;
        while (bulkhead.busyThreads() < threads && System.currentTimeMillis() < giveUpAt) {
            Thread.onSpinWait();
        }
    }
}
