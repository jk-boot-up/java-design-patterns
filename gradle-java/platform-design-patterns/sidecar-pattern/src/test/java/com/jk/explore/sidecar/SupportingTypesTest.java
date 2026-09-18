package com.jk.explore.sidecar;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** The small pieces the rest of the project counts and prints with. */
class SupportingTypesTest {

    @Test
    @DisplayName("the clock records waiting without performing any")
    void theClockDoesNotActuallyWait() {
        Clock clock = new Clock();
        long startedAt = System.nanoTime();

        clock.waitFor(200);
        clock.waitFor(400);

        assertEquals(600, clock.now());
        assertTrue(System.nanoTime() - startedAt < 100_000_000L, "no real sleeping");
    }

    @Test
    @DisplayName("resetting the clock puts it back to the start of the wobble")
    void theClockResets() {
        Clock clock = new Clock();
        clock.waitFor(999);

        clock.reset();

        assertEquals(0, clock.now());
    }

    @Test
    @DisplayName("the call log counts by service in the order they first appeared")
    void theLogKeepsArrivalOrder() {
        CallLog log = new CallLog();
        log.record("subscription-billing", "SUB-1", 0, "declined");
        log.record("subscription-billing", "SUB-1", 10, "charged");
        log.record("checkout", "ORD-1", 0, "charged");

        assertEquals("[subscription-billing, checkout]", log.byService().keySet().toString());
        assertEquals(2, log.countFor("subscription-billing"));
        assertEquals(1, log.countFor("checkout"));
    }

    @Test
    @DisplayName("the call log counts outcomes as well as callers")
    void theLogCountsOutcomes() {
        CallLog log = new CallLog();
        log.record("checkout", "ORD-1", 0, "declined");
        log.record("checkout", "ORD-1", 200, "charged");

        assertEquals(1, log.countOf("declined"));
        assertEquals(1, log.countOf("charged"));
        assertEquals(2, log.total());
    }

    @Test
    @DisplayName("a payment carries an idempotency key so retrying is safe")
    void everyPaymentHasAKey() {
        assertEquals("idem-ORD-4417", Payment.of("ORD-4417", 4799).idempotencyKey());
    }

    @Test
    @DisplayName("a receipt says one attempt in the singular")
    void oneAttemptReadsProperly() {
        assertTrue(new Receipt("ORD-1", "pay_ORD-1", 1, 0).describe().contains("1 attempt,"));
        assertTrue(new Receipt("ORD-1", "pay_ORD-1", 3, 600).describe().contains("3 attempts,"));
    }

    @Test
    @DisplayName("money prints in pounds with two places")
    void moneyPrintsInPounds() {
        assertEquals("£47.99", Money.format(4799));
        assertEquals("£12.99", Money.format(1299));
        assertEquals("£186.40", Money.format(18640));
        assertEquals("£0.05", Money.format(5));
    }

    @Test
    @DisplayName("metrics report attempts, successes and failures under one prefix")
    void metricsReportUnderAPrefix() {
        Metrics metrics = new Metrics("checkout.payments");
        metrics.attempted();
        metrics.attempted();
        metrics.succeeded();
        metrics.failed();

        assertEquals("checkout.payments.attempts=2 checkout.payments.ok=1 "
                + "checkout.payments.failed=1", metrics.line());
    }

    @Test
    @DisplayName("the configuration prints as one readable line")
    void theConfigurationPrintsAsOneLine() {
        assertEquals("maxAttempts=3 firstBackoff=200ms deadline=2000ms tls=TLS1.3",
                SidecarConfig.agreedWithTheProvider().line());
    }
}
