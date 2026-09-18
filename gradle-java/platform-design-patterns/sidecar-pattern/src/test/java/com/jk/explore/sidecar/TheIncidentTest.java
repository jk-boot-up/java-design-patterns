package com.jk.explore.sidecar;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * The night itself, asserted end to end — once with the concerns inside the services and
 * once with them beside the services.
 *
 * <p>Every count here is taken from the gateway's own log rather than from the services,
 * because a service's belief about how many times it tried is exactly the thing that went
 * wrong. If these two tests ever disagree with the demo output, the demo is what the
 * video shows and the documents quote, so one of them is now a lie.
 */
class TheIncidentTest {

    private static final Payment SUBSCRIPTION = Payment.of("SUB-90118", 1299);
    private static final Payment CHECKOUT = Payment.of("ORD-4417", 4799);
    private static final Payment REFUND = Payment.of("REF-3820", 2250);
    private static final Payment PAYOUT = Payment.of("PAY-7741", 18640);

    @Test
    @DisplayName("with the retry code inside the services, the sellers do not get paid")
    void theNightThePayoutsFailed() {
        PaymentGateway gateway = new PaymentGateway();
        gateway.beginWobble();
        SubscriptionBillingService billing = new SubscriptionBillingService(gateway);
        CheckoutService checkout = new CheckoutService(gateway);
        RefundsService refunds = new RefundsService(gateway);
        MarketplacePayoutsService payouts = new MarketplacePayoutsService(gateway);
        checkout.applyPolicyReview();
        refunds.applyPolicyReview();
        payouts.applyPolicyReview();

        // The three services that were updated all succeed. So does the one that was not.
        assertEquals(6, billing.pay(SUBSCRIPTION).attempts());
        assertEquals(3, checkout.pay(CHECKOUT).attempts());
        assertEquals(3, refunds.pay(REFUND).attempts());

        PaymentFailed failed = assertThrows(PaymentFailed.class, () -> payouts.pay(PAYOUT));

        assertEquals(PaymentFailed.Reason.RATE_LIMITED, failed.reason());
        assertEquals(13, gateway.callLog().total());
        assertEquals(1, gateway.callLog().countOf("rate-limited"));
    }

    @Test
    @DisplayName("the service that misbehaved is not the service that suffered")
    void theBlameDoesNotLandWhereTheCauseIs() {
        PaymentGateway gateway = new PaymentGateway();
        gateway.beginWobble();
        SubscriptionBillingService billing = new SubscriptionBillingService(gateway);
        CheckoutService checkout = new CheckoutService(gateway);
        RefundsService refunds = new RefundsService(gateway);
        MarketplacePayoutsService payouts = new MarketplacePayoutsService(gateway);
        checkout.applyPolicyReview();
        refunds.applyPolicyReview();
        payouts.applyPolicyReview();

        billing.pay(SUBSCRIPTION);
        checkout.pay(CHECKOUT);
        refunds.pay(REFUND);
        assertThrows(PaymentFailed.class, () -> payouts.pay(PAYOUT));

        assertEquals(1, billing.metrics().successes(), "the cause of the incident succeeded");
        assertEquals(0, billing.metrics().failures());
        assertEquals(1, payouts.metrics().failures(), "an innocent service took the failure");
        assertTrue(gateway.callLog().countFor("subscription-billing")
                        > gateway.callLog().countFor("marketplace-payouts") * 5,
                "one service spent what another needed");
    }

    @Test
    @DisplayName("with the retry code beside the services, all four payments go through")
    void theSameNightWithSidecars() {
        PaymentGateway gateway = new PaymentGateway();
        gateway.beginWobble();
        SidecarConfig one = SidecarConfig.agreedWithTheProvider();
        List<TakesPayments> services = List.of(
                new ServiceBehindASidecar(SubscriptionBillingService.NAME,
                        new Sidecar(SubscriptionBillingService.NAME, gateway, one)),
                new ServiceBehindASidecar(CheckoutService.NAME,
                        new Sidecar(CheckoutService.NAME, gateway, one)),
                new ServiceBehindASidecar(RefundsService.NAME,
                        new Sidecar(RefundsService.NAME, gateway, one)),
                new ServiceBehindASidecar(MarketplacePayoutsService.NAME,
                        new Sidecar(MarketplacePayoutsService.NAME, gateway, one)));
        List<Payment> payments = List.of(SUBSCRIPTION, CHECKOUT, REFUND, PAYOUT);

        for (int i = 0; i < services.size(); i++) {
            Receipt receipt = services.get(i).pay(payments.get(i));
            assertEquals(3, receipt.attempts());
            assertEquals(603, receipt.waitedMillis());
        }

        assertEquals(PaymentGateway.ATTEMPTS_ALLOWED_PER_WOBBLE, gateway.callLog().total());
        assertEquals(0, gateway.callLog().countOf("rate-limited"));
    }

    @Test
    @DisplayName("the sidecars use exactly the allowance, not less and not more")
    void theAllowanceIsSpentExactly() {
        PaymentGateway gateway = new PaymentGateway();
        gateway.beginWobble();
        SidecarConfig one = SidecarConfig.agreedWithTheProvider();
        for (String service : List.of("subscription-billing", "checkout",
                "refunds", "marketplace-payouts")) {
            new Sidecar(service, gateway, one).send(Payment.of(service + "-1", 100));
            assertEquals(3, gateway.callLog().countFor(service));
        }

        assertEquals(12, gateway.callLog().total());
    }
}
