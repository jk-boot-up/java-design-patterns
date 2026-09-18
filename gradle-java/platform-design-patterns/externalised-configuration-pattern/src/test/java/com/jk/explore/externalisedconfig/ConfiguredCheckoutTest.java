package com.jk.explore.externalisedconfig;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The pattern working as advertised: the same program, quoting differently,
 * without being rebuilt or restarted.
 */
class ConfiguredCheckoutTest {

    private static final String KEY = "delivery.freeOver";
    private static final Basket FORTY_EIGHT = new Basket("ORD-7102", Money.pounds(48));

    private final ChangeLog log = new ChangeLog();
    private final ConfigServer server =
            new ConfigServer(LocalDateTime.of(2025, 3, 7, 16, 30), log);
    private final Checkout checkout = new ConfiguredCheckout(new TrustingSettings(server));

    @Test
    @DisplayName("with nothing configured the shop runs on the compiled-in default")
    void nothingConfiguredMeansTheDefault() {
        DeliveryQuote quote = checkout.quote(FORTY_EIGHT);

        assertEquals(Money.pounds(50), quote.thresholdApplied());
        assertFalse(quote.isFree());
        assertTrue(quote.thresholdCameFrom().contains("default compiled into the code"));
    }

    @Test
    @DisplayName("a configured value takes effect on the very next quote")
    void aChangeTakesEffectImmediately() {
        assertFalse(checkout.quote(FORTY_EIGHT).isFree());

        server.set(KEY, "35", "marketing");

        DeliveryQuote after = checkout.quote(FORTY_EIGHT);
        assertTrue(after.isFree());
        assertEquals(Money.pounds(35), after.thresholdApplied());
        assertEquals("the config server", after.thresholdCameFrom());
    }

    @Test
    @DisplayName("the threshold is read on every quote, not once at construction")
    void theThresholdIsReadEveryTime() {
        // This is the detail that makes the pattern work. If the value were read
        // in the constructor, the second and third quotes below would be stale.
        server.set(KEY, "35", "marketing");
        assertEquals(Money.pounds(35), checkout.quote(FORTY_EIGHT).thresholdApplied());

        server.set(KEY, "60", "marketing");
        assertEquals(Money.pounds(60), checkout.quote(FORTY_EIGHT).thresholdApplied());

        server.set(KEY, "10", "marketing");
        assertEquals(Money.pounds(10), checkout.quote(FORTY_EIGHT).thresholdApplied());
    }

    @Test
    @DisplayName("the shop keeps selling on its default while the source is unreachable")
    void anOutageDoesNotStopTheShop() {
        server.set(KEY, "35", "marketing");
        server.goOffline("the network link to it dropped");

        DeliveryQuote quote = checkout.quote(FORTY_EIGHT);

        assertEquals(Money.pounds(50), quote.thresholdApplied());
        assertTrue(quote.thresholdCameFrom().contains("could not be reached"));
        // And note the cost of surviving: the promotion is silently off.
        assertFalse(quote.isFree());
    }

    @Test
    @DisplayName("the configured and hard-coded checkouts agree when the value agrees")
    void bothCheckoutsBehaveTheSame() {
        server.set(KEY, "50", "marketing");
        Checkout hardCoded = new HardCodedCheckout();

        for (Basket basket : java.util.List.of(
                new Basket("ORD-1", Money.pounds(62)),
                FORTY_EIGHT,
                new Basket("ORD-3", Money.pence(3150)),
                new Basket("ORD-4", Money.pounds(50)))) {
            assertEquals(hardCoded.quote(basket).deliveryCost(),
                    checkout.quote(basket).deliveryCost(), basket.orderId());
        }
    }
}
