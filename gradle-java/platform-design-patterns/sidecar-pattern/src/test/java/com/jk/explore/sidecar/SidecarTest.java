package com.jk.explore.sidecar;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** The proxy, what it buys, and both of the things it charges for. */
class SidecarTest {

    private PaymentGateway gateway;

    @BeforeEach
    void setUp() {
        gateway = new PaymentGateway();
        gateway.behave();
    }

    private Sidecar sidecarBeside(String service) {
        return new Sidecar(service, gateway, SidecarConfig.agreedWithTheProvider());
    }

    @Test
    @DisplayName("a service behind a sidecar takes payments without knowing how")
    void theServiceStillGetsPaid() {
        ServiceBehindASidecar checkout =
                new ServiceBehindASidecar("checkout", sidecarBeside("checkout"));

        Receipt receipt = checkout.pay(Payment.of("ORD-4417", 4799));

        assertEquals("pay_ORD-4417", receipt.providerRef());
        assertEquals(1, receipt.attempts());
    }

    @Test
    @DisplayName("the gateway sees the service's name, not the proxy's")
    void theProxyCallsOnBehalfOfTheService() {
        new ServiceBehindASidecar("refunds", sidecarBeside("refunds"))
                .pay(Payment.of("REF-3820", 2250));

        assertEquals(1, gateway.callLog().countFor("refunds"));
    }

    @Test
    @DisplayName("all four sidecars read one configuration object, not four copies")
    void oneConfigurationForAllOfThem() {
        SidecarConfig one = SidecarConfig.agreedWithTheProvider();
        List<Sidecar> sidecars = List.of(
                new Sidecar("checkout", gateway, one),
                new Sidecar("refunds", gateway, one),
                new Sidecar("subscription-billing", gateway, one),
                new Sidecar("marketplace-payouts", gateway, one));

        for (Sidecar sidecar : sidecars) {
            assertSame(one, sidecar.config(), "every sidecar must read the same one");
        }
    }

    @Test
    @DisplayName("the proxy retries exactly as the one configuration says")
    void retriesAccordingToTheOneConfiguration() {
        gateway.beginWobble();
        gateway.stopEnforcingQuota();

        Receipt receipt = sidecarBeside("checkout").send(Payment.of("ORD-4417", 4799));

        assertEquals(SidecarConfig.agreedWithTheProvider().maxAttempts(), receipt.attempts());
    }

    @Test
    @DisplayName("the hop costs one millisecond per attempt and nothing else")
    void theHopIsTheOnlyDifference() {
        gateway.beginWobble();
        gateway.stopEnforcingQuota();
        Receipt viaProxy = sidecarBeside("checkout").send(Payment.of("ORD-4417", 4799));

        PaymentGateway direct = new PaymentGateway();
        direct.beginWobble();
        direct.stopEnforcingQuota();
        CheckoutService inProcess = new CheckoutService(direct);
        inProcess.applyPolicyReview();
        Receipt withoutProxy = inProcess.pay(Payment.of("ORD-4417", 4799));

        assertEquals(withoutProxy.attempts(), viaProxy.attempts());
        assertEquals(withoutProxy.waitedMillis() + Sidecar.HOP_MILLIS * viaProxy.attempts(),
                viaProxy.waitedMillis());
    }

    @Test
    @DisplayName("a stopped sidecar fails every call before it leaves the machine")
    void aStoppedSidecarFailsEverything() {
        Sidecar sidecar = sidecarBeside("checkout");
        ServiceBehindASidecar checkout = new ServiceBehindASidecar("checkout", sidecar);
        sidecar.stop();

        PaymentFailed failed = assertThrows(PaymentFailed.class,
                () -> checkout.pay(Payment.of("ORD-4417", 4799)));

        assertEquals(PaymentFailed.Reason.NOTHING_LISTENING, failed.reason());
        assertEquals(0, gateway.callLog().total(), "nothing reached the gateway");
        assertFalse(sidecar.running());
    }

    @Test
    @DisplayName("the service behind a stopped sidecar has no retry of its own left")
    void theServiceCannotFallBack() {
        Sidecar sidecar = sidecarBeside("checkout");
        ServiceBehindASidecar checkout = new ServiceBehindASidecar("checkout", sidecar);
        sidecar.stop();

        assertThrows(PaymentFailed.class, () -> checkout.pay(Payment.of("ORD-4417", 4799)));
        assertThrows(PaymentFailed.class, () -> checkout.pay(Payment.of("ORD-4418", 4799)));

        assertEquals(0, sidecar.metrics().attempts());
    }

    @Test
    @DisplayName("restarting the sidecar restores the service without touching it")
    void restartingTheProxyIsEnough() {
        Sidecar sidecar = sidecarBeside("checkout");
        ServiceBehindASidecar checkout = new ServiceBehindASidecar("checkout", sidecar);
        sidecar.stop();
        assertThrows(PaymentFailed.class, () -> checkout.pay(Payment.of("ORD-4417", 4799)));

        sidecar.start();

        assertEquals("pay_ORD-4417", checkout.pay(Payment.of("ORD-4417", 4799)).providerRef());
    }

    @Test
    @DisplayName("every proxy reports its counters under the same name")
    void theCountersAreNamedOnceForEverybody() {
        assertEquals("sidecar.payments", sidecarBeside("checkout").metrics().prefix());
        assertEquals("sidecar.payments", sidecarBeside("refunds").metrics().prefix());
    }

    @Test
    @DisplayName("a refusal is not retried by the proxy either")
    void theProxyDoesNotRetryARefusal() {
        for (int i = 0; i < PaymentGateway.ATTEMPTS_ALLOWED_PER_WOBBLE; i++) {
            gateway.charge("subscription-billing", Payment.of("SUB-" + i, 100), 0);
        }
        Sidecar sidecar = sidecarBeside("checkout");

        assertThrows(PaymentFailed.class, () -> sidecar.send(Payment.of("ORD-4417", 4799)));

        assertEquals(1, gateway.callLog().countFor("checkout"));
    }

    @Test
    @DisplayName("changing the policy is one object, not four edits")
    void changingThePolicyIsOneChange() {
        assertEquals(1, Concerns.placesToEditAPolicyWithSidecars());
        assertEquals(6, SidecarConfig.beforeTheReview().maxAttempts());
        assertEquals(3, SidecarConfig.agreedWithTheProvider().maxAttempts());
    }

    @Test
    @DisplayName("the configuration holds nothing about checkout, refunds or payouts")
    void theConfigurationHoldsNoBusinessRules() {
        String written = SidecarConfig.agreedWithTheProvider().line();

        assertFalse(written.contains("checkout"));
        assertFalse(written.contains("refund"));
        assertFalse(written.contains("payout"));
    }
}
