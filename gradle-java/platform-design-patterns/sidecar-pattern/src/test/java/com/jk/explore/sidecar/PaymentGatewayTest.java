package com.jk.explore.sidecar;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * The gateway is the only thing in this project that nobody in the shop controls, so its
 * behaviour has to be exact. Every other number in the demo is derived from these rules.
 */
class PaymentGatewayTest {

    private PaymentGateway gateway;

    @BeforeEach
    void setUp() {
        gateway = new PaymentGateway();
    }

    @Test
    @DisplayName("a healthy gateway takes the money on the first attempt")
    void healthyGatewaySucceedsImmediately() {
        gateway.behave();

        assertEquals("pay_ORD-1", gateway.charge("checkout", Payment.of("ORD-1", 100), 0));
        assertEquals(1, gateway.callLog().total());
    }

    @Test
    @DisplayName("during a wobble, an attempt before the recovery moment is declined")
    void declinesBeforeRecovery() {
        gateway.beginWobble();

        PaymentFailed failed = assertThrows(PaymentFailed.class,
                () -> gateway.charge("checkout", Payment.of("ORD-1", 100), 299));
        assertEquals(PaymentFailed.Reason.WOBBLE, failed.reason());
    }

    @Test
    @DisplayName("an attempt exactly at the recovery moment succeeds")
    void succeedsExactlyAtRecovery() {
        gateway.beginWobble();

        assertNotNull(gateway.charge("checkout", Payment.of("ORD-1", 100),
                PaymentGateway.RECOVERS_AT_MILLIS));
    }

    @Test
    @DisplayName("the idempotency key means a repeat returns the first reference")
    void repeatIsNotASecondCharge() {
        gateway.behave();
        Payment payment = Payment.of("ORD-1", 100);

        String first = gateway.charge("checkout", payment, 0);
        String second = gateway.charge("checkout", payment, 5);

        assertEquals(first, second);
    }

    @Test
    @DisplayName("the allowance is spent across the whole account, not per service")
    void allowanceIsSharedAcrossServices() {
        gateway.behave();
        for (int i = 0; i < PaymentGateway.ATTEMPTS_ALLOWED_PER_WOBBLE; i++) {
            gateway.charge("subscription-billing", Payment.of("SUB-" + i, 100), 0);
        }

        PaymentFailed failed = assertThrows(PaymentFailed.class,
                () -> gateway.charge("checkout", Payment.of("ORD-1", 100), 0));

        assertEquals(PaymentFailed.Reason.RATE_LIMITED, failed.reason());
    }

    @Test
    @DisplayName("a refused attempt is still an attempt the gateway saw and logged")
    void refusedAttemptsAreLogged() {
        gateway.behave();
        for (int i = 0; i < PaymentGateway.ATTEMPTS_ALLOWED_PER_WOBBLE; i++) {
            gateway.charge("subscription-billing", Payment.of("SUB-" + i, 100), 0);
        }

        assertThrows(PaymentFailed.class,
                () -> gateway.charge("checkout", Payment.of("ORD-1", 100), 0));

        assertEquals(1, gateway.callLog().countOf("rate-limited"));
        assertEquals(PaymentGateway.ATTEMPTS_ALLOWED_PER_WOBBLE + 1, gateway.callLog().total());
    }

    @Test
    @DisplayName("the allowance is three attempts each for the four paying services")
    void theAllowanceIsTheContract() {
        assertEquals(12, PaymentGateway.ATTEMPTS_ALLOWED_PER_WOBBLE);
        assertEquals(3 * 4, PaymentGateway.ATTEMPTS_ALLOWED_PER_WOBBLE);
    }
}
