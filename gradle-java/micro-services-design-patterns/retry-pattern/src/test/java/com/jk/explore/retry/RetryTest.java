package com.jk.explore.retry;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * What a careful retry must guarantee.
 *
 * Every test in here is really one of two questions: did the shopper get through,
 * and was the card charged exactly once. The second question is the one that keeps
 * people awake.
 */
class RetryTest {

    private static final String ORDER = "ORD-5001";
    private static final Money AMOUNT = Money.pence(44999);
    private static final long SEED = 7L;

    private SimulatedClock clock;
    private CallLog log;
    private PaymentGateway payments;

    @BeforeEach
    void setUp() {
        clock = new SimulatedClock();
        log = new CallLog(clock);
        payments = new PaymentGateway(clock, log);
    }

    private CheckoutService checkout() {
        return new CheckoutService(payments, RetryPolicy.threeAttempts(SEED), clock, log);
    }

    // ------------------------------------------------- the case retrying is for

    @Test
    @DisplayName("a checkout that would have failed succeeds on the second attempt")
    void aTransientTimeoutRecovers() {
        payments.timeOutNext(1);

        Receipt receipt = checkout().pay(ORDER, AMOUNT);

        assertEquals(ORDER, receipt.orderId());
        assertEquals(2, payments.attempts());
    }

    @Test
    @DisplayName("two timeouts in a row still leave one attempt, and it works")
    void twoTimeoutsStillRecover() {
        payments.timeOutNext(2);

        assertEquals(AMOUNT, checkout().pay(ORDER, AMOUNT).amount());
        assertEquals(3, payments.attempts());
    }

    @Test
    @DisplayName("three timeouts exhaust the policy and the failure is reported honestly")
    void itGivesUpEventually() {
        payments.timeOutNext(3);

        assertThrows(GatewayTimeoutException.class, () -> checkout().pay(ORDER, AMOUNT));
        assertEquals(3, payments.attempts());
        assertEquals(0, payments.charges().size());
    }

    @Test
    @DisplayName("a recovered checkout charges the card exactly once")
    void recoveringDoesNotChargeTwice() {
        payments.timeOutNext(1);

        checkout().pay(ORDER, AMOUNT);

        assertEquals(1, payments.charges().size());
        assertEquals(AMOUNT, payments.totalCharged());
    }

    // ----------------------------------------------------------- the waiting

    @Test
    @DisplayName("the first attempt does not wait, and later attempts wait longer each time")
    void theWaitsGetLonger() {
        RetryPolicy policy = RetryPolicy.threeAttempts(SEED);

        assertEquals(0, policy.baseDelayBeforeAttempt(1));
        assertEquals(100, policy.baseDelayBeforeAttempt(2));
        assertEquals(200, policy.baseDelayBeforeAttempt(3));
        assertEquals(400, policy.baseDelayBeforeAttempt(4));
    }

    @Test
    @DisplayName("jitter keeps the wait within its promised band, above the base and not far above")
    void jitterStaysInItsBand() {
        RetryPolicy policy = RetryPolicy.threeAttempts(SEED);

        for (int i = 0; i < 50; i++) {
            long delay = policy.delayBeforeAttempt(2);
            assertTrue(delay >= 100 && delay <= 120,
                    "100ms plus up to 20% jitter, got " + delay + "ms");
        }
    }

    @Test
    @DisplayName("two callers that fail together do not retry together")
    void jitterSeparatesCallers() {
        RetryPolicy first = RetryPolicy.threeAttempts(1L);
        RetryPolicy second = RetryPolicy.threeAttempts(2L);

        boolean everDiffered = false;
        for (int i = 0; i < 20; i++) {
            if (first.delayBeforeAttempt(2) != second.delayBeforeAttempt(2)) {
                everDiffered = true;
            }
        }
        assertTrue(everDiffered, "without jitter every caller retries in unison");
    }

    @Test
    @DisplayName("retrying costs the shopper real time, and the timeline says how much")
    void waitingIsNotFree() {
        payments.timeOutNext(2);
        Retrier retrier = new Retrier(RetryPolicy.threeAttempts(SEED), clock, log);
        PaymentRequest request = PaymentRequest.forOrder(ORDER, AMOUNT);

        retrier.call("payment", () -> payments.charge(request));

        // three attempts at 50ms each, plus roughly 100ms and 200ms of waiting
        assertEquals(3, retrier.attemptsMade());
        assertTrue(retrier.waitedMillis() >= 300 && retrier.waitedMillis() <= 360,
                "waited " + retrier.waitedMillis() + "ms");
        assertTrue(log.elapsedMillis() > 400,
                "the shopper waited " + log.elapsedMillis() + "ms for this");
    }

    // ------------------------------------------- telling the failures apart

    @Test
    @DisplayName("a declined card is not retried even once")
    void aPermanentFailureIsNotRetried() {
        payments.declineAlways();

        assertThrows(CardDeclinedException.class, () -> checkout().pay(ORDER, AMOUNT));
        assertEquals(1, payments.attempts());
    }

    @Test
    @DisplayName("a declined card is reported immediately, not after three delays")
    void aPermanentFailureIsFast() {
        payments.declineAlways();

        assertThrows(CardDeclinedException.class, () -> checkout().pay(ORDER, AMOUNT));
        assertEquals(PaymentGateway.GATEWAY_LATENCY_MILLIS, clock.millis());
    }

    @Test
    @DisplayName("the retrier tells the shopper which kind of failure it was")
    void theTimelineNamesTheDecision() {
        payments.declineAlways();

        assertThrows(CardDeclinedException.class, () -> checkout().pay(ORDER, AMOUNT));
        assertTrue(log.timeline().contains("PERMANENT"),
                "the decision not to retry should be visible:\n" + log.timeline());
    }

    // --------------------------------------- the failure that charges the card

    @Test
    @DisplayName("a lost reply after a real charge does not charge the card twice")
    void aLostReplyDoesNotDoubleCharge() {
        payments.loseReplyAfterCharging(1);

        Receipt receipt = checkout().pay(ORDER, AMOUNT);

        assertEquals(1, payments.charges().size());
        assertEquals(AMOUNT, payments.totalCharged());
        assertEquals("chg-1", receipt.chargeId(),
                "the retry should hand back the charge that was already made");
    }

    @Test
    @DisplayName("the safety comes from the key being the same on every attempt")
    void everyAttemptCarriesTheSameKey() {
        PaymentRequest first = PaymentRequest.forOrder(ORDER, AMOUNT);
        PaymentRequest second = PaymentRequest.forOrder(ORDER, AMOUNT);

        assertEquals(first.idempotencyKey(), second.idempotencyKey());
    }

    @Test
    @DisplayName("the gateway charges a repeated key once and says it is replaying")
    void theGatewayRecognisesARepeat() {
        PaymentRequest request = PaymentRequest.forOrder(ORDER, AMOUNT);

        Receipt first = payments.charge(request);
        Receipt again = payments.charge(request);

        assertEquals(first, again);
        assertEquals(1, payments.charges().size());
        assertTrue(log.timeline().contains("REPLAYED"));
    }

    @Test
    @DisplayName("a policy that never tries is refused")
    void aPolicyMustAllowAtLeastOneAttempt() {
        assertThrows(IllegalArgumentException.class,
                () -> new RetryPolicy(0, 100, 2, 20, SEED));
    }
}
