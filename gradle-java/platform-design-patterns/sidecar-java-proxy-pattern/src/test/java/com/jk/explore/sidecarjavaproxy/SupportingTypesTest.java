package com.jk.explore.sidecarjavaproxy;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * The small pieces every other test stands on: money, the clock, the provider's log, and
 * the promise that makes retrying legal at all.
 */
class SupportingTypesTest {

    @Test
    @DisplayName("pence come out as pounds with two decimal places")
    void formatsMoney() {
        assertEquals("£47.99", Money.format(4799));
        assertEquals("£31.50", Money.format(3150));
        assertEquals("£0.05", Money.format(5));
    }

    @Test
    @DisplayName("the clock only moves when something says it waited")
    void theClockIsMovedByHand() {
        Clock clock = new Clock();

        assertEquals(0, clock.now());
        clock.waitFor(200);
        clock.waitFor(400);
        assertEquals(600, clock.now());
        clock.reset();
        assertEquals(0, clock.now());
    }

    @Test
    @DisplayName("a repeated payment is charged once and returns the first reference")
    void theIdempotencyKeyMakesRetryingSafe() {
        PaymentGateway provider = new PaymentGateway();
        provider.behave();
        Payment payment = Payment.of("ORD-9", 100);

        String first = provider.charge("checkout", payment, 0);
        String second = provider.charge("checkout", payment, 5);

        assertEquals(first, second);
        // Two attempts really did arrive; only one charge came of them.
        assertEquals(2, provider.callLog().total());
    }

    @Test
    @DisplayName("the span of an empty log is zero rather than an exception")
    void anEmptyLogSpansNothing() {
        assertEquals(0, new CallLog().spanMillis());
    }

    @Test
    @DisplayName("a wobbling provider declines anything asked before it recovers")
    void theWobbleIsExact() {
        PaymentGateway provider = new PaymentGateway();
        provider.beginWobble();
        Payment payment = Payment.of("ORD-10", 100);

        assertThrows(PaymentFailed.class,
                () -> provider.charge("checkout", payment,
                        PaymentGateway.RECOVERS_AT_MILLIS - 1));
        assertEquals("pay_ORD-10", provider.charge("checkout", payment,
                PaymentGateway.RECOVERS_AT_MILLIS));
    }

    @Test
    @DisplayName("the receipt reports attempts made, not calls asked for")
    void theReceiptDescribesItself() {
        assertEquals("pay_X (1 attempt, 1ms waiting)",
                new Receipt("X", "pay_X", 1, 1).describe());
        assertEquals("pay_X (3 attempts, 603ms waiting)",
                new Receipt("X", "pay_X", 3, 603).describe());
    }

    @Test
    @DisplayName("the agreed policy is the one both proxies are handed")
    void thePolicyReadsBackAsAgreed() {
        assertEquals("maxAttempts=3 firstBackoff=200ms deadline=2000ms tls=TLS1.3",
                ProxyPolicy.agreedWithTheProvider().line());
    }
}
