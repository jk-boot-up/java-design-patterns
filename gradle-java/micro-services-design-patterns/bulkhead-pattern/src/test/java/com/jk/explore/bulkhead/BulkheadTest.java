package com.jk.explore.bulkhead;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The one project in this category with real threads, and therefore the one that has
 * to be careful.
 *
 * No test sleeps. A slow partner API is a closed {@link Gate}, so a job holds its
 * thread for exactly as long as the test wants it to; and where a test has to prove
 * that something is <em>not</em> happening, it uses a short bounded
 * {@code Future.get} rather than a guess about timing.
 */
class BulkheadTest {

    /** How long a shopper would wait. Long enough to be fair, short enough to be quick. */
    private static final long PATIENCE_MILLIS = 250;

    private JobLog log;
    private Gate partnerApi;
    private final List<Bulkhead> open = new ArrayList<>();

    @BeforeEach
    void setUp() {
        log = new JobLog();
        partnerApi = new Gate();
    }

    @AfterEach
    void releaseEverything() {
        partnerApi.open();
        open.forEach(Bulkhead::close);
    }

    private Bulkhead bulkhead(String name, int threads, int queue) {
        Bulkhead bulkhead = new Bulkhead(name, threads, queue, log);
        open.add(bulkhead);
        return bulkhead;
    }

    /** Fills a bulkhead with feed jobs and waits until its threads have picked them up. */
    private void jamWithFeedJobs(Bulkhead bulkhead, int jobs) {
        SupplierFeed feed = new SupplierFeed(partnerApi);
        for (int i = 1; i <= jobs; i++) {
            bulkhead.submit("feed-" + i, feed.importBatch(i));
        }
        long giveUpAt = System.currentTimeMillis() + 5_000;
        while (bulkhead.busyThreads() < Math.min(jobs, bulkhead.size())
                && System.currentTimeMillis() < giveUpAt) {
            Thread.onSpinWait();
        }
        assertEquals(Math.min(jobs, bulkhead.size()), bulkhead.busyThreads(),
                "the feed jobs should be holding threads before the test continues");
    }

    // ------------------------------------------------------- the shared pool sinks

    @Test
    @DisplayName("with one shared pool, a slow feed starves checkout of threads")
    void oneSharedPoolStarvesCheckout() {
        Bulkhead shared = bulkhead("shared", 4, 4);
        jamWithFeedJobs(shared, 4);

        Future<String> sale = shared.submit("checkout", new Checkout().takePayment("ORD-5001"));

        assertThrows(TimeoutException.class,
                () -> sale.get(PATIENCE_MILLIS, TimeUnit.MILLISECONDS),
                "checkout is fine and fast; it simply cannot get a thread");
    }

    @Test
    @DisplayName("the starved checkout is not broken -- it runs the moment a thread frees up")
    void theStarvedCheckoutWasNeverBroken() throws Exception {
        Bulkhead shared = bulkhead("shared", 4, 4);
        jamWithFeedJobs(shared, 4);
        Future<String> sale = shared.submit("checkout", new Checkout().takePayment("ORD-5001"));

        partnerApi.open();

        assertEquals("paid ORD-5001", sale.get(5, TimeUnit.SECONDS));
    }

    // ---------------------------------------------------------- the partition holds

    @Test
    @DisplayName("with two bulkheads, checkout is served while the feed is jammed")
    void aPartitionKeepsTheShopSelling() throws Exception {
        Bulkhead feedPool = bulkhead("feed", 2, 2);
        Bulkhead checkoutPool = bulkhead("checkout", 2, 2);
        jamWithFeedJobs(feedPool, 4);

        Future<String> sale = checkoutPool.submit("checkout",
                new Checkout().takePayment("ORD-5001"));

        assertEquals("paid ORD-5001", sale.get(PATIENCE_MILLIS, TimeUnit.MILLISECONDS));
    }

    @Test
    @DisplayName("the feed really is jammed at the same time, so the isolation is the reason")
    void theFeedIsGenuinelyStuck() throws Exception {
        Bulkhead feedPool = bulkhead("feed", 2, 2);
        Bulkhead checkoutPool = bulkhead("checkout", 2, 2);
        jamWithFeedJobs(feedPool, 4);

        checkoutPool.submit("checkout", new Checkout().takePayment("ORD-5001"))
                .get(PATIENCE_MILLIS, TimeUnit.MILLISECONDS);

        assertEquals(2, feedPool.busyThreads());
        assertEquals(2, feedPool.queued());
    }

    @Test
    @DisplayName("many sales go through while the feed sits stuck")
    void checkoutKeepsWorkingIndefinitely() throws Exception {
        Bulkhead feedPool = bulkhead("feed", 2, 2);
        Bulkhead checkoutPool = bulkhead("checkout", 2, 2);
        jamWithFeedJobs(feedPool, 4);

        for (int i = 0; i < 20; i++) {
            Future<String> sale = checkoutPool.submit("checkout",
                    new Checkout().takePayment("ORD-" + i));
            assertEquals("paid ORD-" + i, sale.get(PATIENCE_MILLIS, TimeUnit.MILLISECONDS));
        }
    }

    @Test
    @DisplayName("the feed's threads belong to the feed and nothing else")
    void poolsDoNotBorrowFromEachOther() throws Exception {
        Bulkhead feedPool = bulkhead("feed", 2, 2);
        Bulkhead checkoutPool = bulkhead("checkout", 2, 2);
        jamWithFeedJobs(feedPool, 2);

        checkoutPool.submit("checkout", new Checkout().takePayment("ORD-5001"))
                .get(PATIENCE_MILLIS, TimeUnit.MILLISECONDS);

        assertTrue(log.entries().stream()
                        .filter(e -> e.job().equals("checkout"))
                        .allMatch(e -> e.what().contains("checkout-worker")
                                || e.what().equals("finished")),
                "checkout ran on checkout's own threads:\n" + log.timeline());
    }

    // ------------------------------------------------------- refusing, and the cost

    @Test
    @DisplayName("a full bulkhead refuses the next job instead of queueing it")
    void afullBulkheadRefuses() {
        Bulkhead feedPool = bulkhead("feed", 2, 2);
        jamWithFeedJobs(feedPool, 4);

        BulkheadFullException full = assertThrows(BulkheadFullException.class,
                () -> feedPool.submit("feed-5", new SupplierFeed(partnerApi).importBatch(5)));

        assertEquals("feed", full.bulkheadName());
        assertEquals(4, feedPool.accepted());
        assertEquals(1, feedPool.rejected());
    }

    @Test
    @DisplayName("the refusal is immediate, so the caller can do something else")
    void theRefusalIsFast() {
        Bulkhead feedPool = bulkhead("feed", 2, 2);
        jamWithFeedJobs(feedPool, 4);

        long startedAt = System.currentTimeMillis();
        assertThrows(BulkheadFullException.class,
                () -> feedPool.submit("feed-5", new SupplierFeed(partnerApi).importBatch(5)));

        assertTrue(System.currentTimeMillis() - startedAt < PATIENCE_MILLIS,
                "a refusal that takes as long as the work would defeat the point");
    }

    @Test
    @DisplayName("partitioning leaves threads idle beside work that is waiting -- the honest cost")
    void isolationIsPaidForInIdleThreads() {
        Bulkhead feedPool = bulkhead("feed", 2, 2);
        Bulkhead checkoutPool = bulkhead("checkout", 2, 2);
        jamWithFeedJobs(feedPool, 4);

        assertEquals(2, feedPool.queued(), "two batches waiting for a thread");
        assertEquals(2, checkoutPool.idleThreads(), "two threads with nothing to do");
    }

    @Test
    @DisplayName("one pool of four would have run all four batches at once")
    void thesharedPoolIsFasterOnAGoodDay() {
        Bulkhead shared = bulkhead("shared", 4, 4);
        jamWithFeedJobs(shared, 4);

        assertEquals(4, shared.busyThreads());
        assertEquals(0, shared.queued(),
                "nothing waiting -- which is exactly why the shared pool is tempting");
    }

    @Test
    @DisplayName("the timeline records which pool ran what")
    void theTimelineIsReadable() throws Exception {
        Bulkhead feedPool = bulkhead("feed", 2, 2);
        Bulkhead checkoutPool = bulkhead("checkout", 2, 2);
        jamWithFeedJobs(feedPool, 2);
        checkoutPool.submit("checkout", new Checkout().takePayment("ORD-5001"))
                .get(PATIENCE_MILLIS, TimeUnit.MILLISECONDS);

        assertEquals(2, log.countFor("feed"), "two feed jobs started, neither finished yet");
        assertEquals(2, log.countFor("checkout"), "one checkout started and finished");
    }
}
