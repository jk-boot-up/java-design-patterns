package com.jk.explore.sidecar;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * The four services, before anything is moved out of them.
 *
 * <p>The test worth reading twice is {@link #billingHasNoWayToApplyTheReview()}. It does
 * not assert that the billing service is wrong — it asserts that there is no method on it
 * to make it right, which is a much stronger statement and the actual shape of the
 * problem. Three services could be updated because somebody opened three files. The
 * fourth stayed as it was because nothing in the shop's code, build or tests knows that a
 * fourth file exists.
 */
class CopiedConcernsTest {

    private PaymentGateway gateway;

    @BeforeEach
    void setUp() {
        gateway = new PaymentGateway();
        gateway.behave();
    }

    @Test
    @DisplayName("all four services start from the same pre-review settings")
    void allFourStartTheSame() {
        Settings expected = new Settings(6, 10, 2_000, "TLS1.3");

        assertEquals(expected, new CheckoutService(gateway).settings());
        assertEquals(expected, new RefundsService(gateway).settings());
        assertEquals(expected, new MarketplacePayoutsService(gateway).settings());
        assertEquals(expected, new SubscriptionBillingService(gateway).settings());
    }

    @Test
    @DisplayName("the review changes checkout, refunds and payouts")
    void theReviewLandsInThree() {
        CheckoutService checkout = new CheckoutService(gateway);
        RefundsService refunds = new RefundsService(gateway);
        MarketplacePayoutsService payouts = new MarketplacePayoutsService(gateway);
        checkout.applyPolicyReview();
        refunds.applyPolicyReview();
        payouts.applyPolicyReview();

        Settings agreed = new Settings(3, 200, 2_000, "TLS1.3");
        assertEquals(agreed, checkout.settings());
        assertEquals(agreed, refunds.settings());
        assertEquals(agreed, payouts.settings());
    }

    @Test
    @DisplayName("subscription billing has no method that applies the review at all")
    void billingHasNoWayToApplyTheReview() {
        List<String> methods = List.of(SubscriptionBillingService.class.getDeclaredMethods())
                .stream()
                .map(method -> method.getName())
                .toList();

        assertTrue(methods.contains("pay"), "it still takes payments");
        assertTrue(methods.contains("settings"), "it still reports its settings");
        assertTrue(!methods.contains("applyPolicyReview"),
                "the point of this project is that nobody wrote this method here");
    }

    @Test
    @DisplayName("after the review the fourth service still disagrees with the other three")
    void billingDisagreesWithTheRest() {
        CheckoutService checkout = new CheckoutService(gateway);
        checkout.applyPolicyReview();

        assertNotEquals(checkout.settings(), new SubscriptionBillingService(gateway).settings());
    }

    @Test
    @DisplayName("the pre-review policy really does spend six attempts on one payment")
    void theOldPolicySpendsSixAttempts() {
        gateway.beginWobble();
        gateway.stopEnforcingQuota();

        Receipt receipt = new SubscriptionBillingService(gateway).pay(Payment.of("SUB-1", 1299));

        assertEquals(6, receipt.attempts());
        assertEquals(310, receipt.waitedMillis());
    }

    @Test
    @DisplayName("the agreed policy spends three attempts on the same payment")
    void theAgreedPolicySpendsThree() {
        gateway.beginWobble();
        gateway.stopEnforcingQuota();
        CheckoutService checkout = new CheckoutService(gateway);
        checkout.applyPolicyReview();

        Receipt receipt = checkout.pay(Payment.of("ORD-1", 4799));

        assertEquals(3, receipt.attempts());
        assertEquals(600, receipt.waitedMillis());
    }

    @Test
    @DisplayName("a service refused for asking too often does not ask again")
    void doesNotRetryARefusal() {
        gateway.behave();
        for (int i = 0; i < PaymentGateway.ATTEMPTS_ALLOWED_PER_WOBBLE; i++) {
            gateway.charge("subscription-billing", Payment.of("SUB-" + i, 100), 0);
        }
        CheckoutService checkout = new CheckoutService(gateway);
        checkout.applyPolicyReview();

        assertThrows(PaymentFailed.class, () -> checkout.pay(Payment.of("ORD-1", 4799)));

        assertEquals(1, gateway.callLog().countFor("checkout"));
    }

    @Test
    @DisplayName("every service keeps its own counters, under its own name")
    void everyServiceCountsSeparately() {
        assertEquals("checkout.payments", new CheckoutService(gateway).metrics().prefix());
        assertEquals("refunds.payments", new RefundsService(gateway).metrics().prefix());
        assertEquals("billing.payments",
                new SubscriptionBillingService(gateway).metrics().prefix());
        assertEquals("payouts.payments",
                new MarketplacePayoutsService(gateway).metrics().prefix());
    }

    @Test
    @DisplayName("a service's own counters cannot see the other three")
    void countersShowOnlyAQuarterOfThePicture() {
        gateway.behave();
        CheckoutService checkout = new CheckoutService(gateway);
        RefundsService refunds = new RefundsService(gateway);
        checkout.pay(Payment.of("ORD-1", 4799));
        refunds.pay(Payment.of("REF-1", 2250));

        assertEquals(1, checkout.metrics().attempts());
        assertEquals(2, gateway.callLog().total());
    }
}
