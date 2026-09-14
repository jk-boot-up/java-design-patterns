package com.jk.explore.retry;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

/**
 * The three-times loop, tested honestly.
 *
 * Every test here passes, including the one where the customer is charged twice.
 * That is the point of writing them: the double charge is not an exception, not a
 * log line and not a failing build. It is a correct-looking order and a shopper
 * ringing up two days later.
 */
class NaiveCheckoutServiceTest {

    private static final String ORDER = "ORD-5001";
    private static final Money AMOUNT = Money.pence(44999);

    private SimulatedClock clock;
    private CallLog log;
    private PaymentGateway payments;

    @BeforeEach
    void setUp() {
        clock = new SimulatedClock();
        log = new CallLog(clock);
        payments = new PaymentGateway(clock, log);
    }

    private NaiveCheckoutService naiveCheckout() {
        return new NaiveCheckoutService(payments, log);
    }

    @Test
    @DisplayName("it does rescue a checkout from a timeout, which is why it survives review")
    void itLooksLikeItWorks() {
        payments.timeOutNext(1);

        Receipt receipt = naiveCheckout().pay(ORDER, AMOUNT);

        assertEquals(ORDER, receipt.orderId());
        assertEquals(1, payments.charges().size());
    }

    @Test
    @DisplayName("a lost reply charges the shopper twice for one order")
    void itDoubleChargesOnALostReply() {
        payments.loseReplyAfterCharging(1);

        Receipt receipt = naiveCheckout().pay(ORDER, AMOUNT);

        assertEquals(2, payments.charges().size(), "one order, two charges");
        assertEquals(Money.pence(89998), payments.totalCharged());
        assertEquals("chg-2", receipt.chargeId(),
                "and the order records the second charge, so the first one is invisible");
    }

    @Test
    @DisplayName("the double charge happens because each attempt invents a new key")
    void itSendsADifferentKeyEachTime() {
        PaymentRequest first = new PaymentRequest(ORDER, AMOUNT, "key-" + ORDER + "-attempt-1");
        PaymentRequest second = new PaymentRequest(ORDER, AMOUNT, "key-" + ORDER + "-attempt-2");

        assertNotEquals(first.idempotencyKey(), second.idempotencyKey());
    }

    @Test
    @DisplayName("it retries a declined card three times and is told no three times")
    void itRetriesWhatCannotBeRetried() {
        payments.declineAlways();

        assertThrows(CardDeclinedException.class, () -> naiveCheckout().pay(ORDER, AMOUNT));
        assertEquals(3, payments.attempts(),
                "three trips to the bank to hear the same 'no' the first one gave");
        assertEquals(0, payments.charges().size());
    }

    @Test
    @DisplayName("it retries with no delay at all, so a struggling gateway gets no room")
    void itDoesNotWait() {
        payments.timeOutNext(2);

        naiveCheckout().pay(ORDER, AMOUNT);

        // Only the gateway's own 50ms per attempt. Nothing was spent waiting.
        assertEquals(3 * PaymentGateway.GATEWAY_LATENCY_MILLIS, clock.millis());
    }
}
