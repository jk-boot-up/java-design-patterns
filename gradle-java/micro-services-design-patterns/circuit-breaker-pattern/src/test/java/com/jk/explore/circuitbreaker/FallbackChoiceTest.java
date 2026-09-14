package com.jk.explore.circuitbreaker;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The half of the pattern the tutorials skip: what to do while the breaker is open.
 *
 * The same breaker, wrapped around two dependencies, must behave differently. Missing
 * suggestions are something a shop can live without; missing payment is not.
 */
class FallbackChoiceTest {

    private static final String SKU = "SKU-1234";
    private static final Money AMOUNT = Money.pence(44999);
    private static final int THRESHOLD = 3;
    private static final long RESET_AFTER = 5_000;

    private SimulatedClock clock;
    private CallLog log;

    @BeforeEach
    void setUp() {
        clock = new SimulatedClock();
        log = new CallLog(clock);
    }

    private CircuitBreaker breakerFor(String service) {
        return new CircuitBreaker(service, THRESHOLD, RESET_AFTER, clock, log);
    }

    // ------------------------------------------------ optional: hide it, and say so

    @Test
    @DisplayName("the product page is still served when Recommendations is down")
    void theOptionalFeatureDegrades() {
        RecommendationsService down = new RecommendationsService(clock, log).goDown();
        ProductPageService pages = new ProductPageService(down, breakerFor("Recommendations"), log);

        ProductPage page = assertDoesNotThrow(() -> pages.page(SKU));

        assertEquals("Barista Pro Espresso Machine", page.name());
        assertEquals(0, page.suggestions().size());
        assertTrue(page.degraded(), "the page must admit that something was left out");
    }

    @Test
    @DisplayName("once the breaker opens, pages cost nothing at all to serve")
    void anOpenBreakerServesPagesInstantly() {
        RecommendationsService down = new RecommendationsService(clock, log).goDown();
        CircuitBreaker breaker = breakerFor("Recommendations");
        ProductPageService pages = new ProductPageService(down, breaker, log);

        for (int i = 0; i < 3; i++) {
            pages.page(SKU);
        }
        long afterTripping = clock.millis();

        for (int i = 0; i < 20; i++) {
            pages.page(SKU);
        }

        assertEquals(afterTripping, clock.millis(), "twenty pages, no time spent");
        assertEquals(3, down.callsReceived(), "and the broken service was left alone");
        assertEquals(20, breaker.callsRefused());
    }

    @Test
    @DisplayName("only the first three shoppers pay the timeout")
    void theOutageIsPaidForOnce() {
        RecommendationsService down = new RecommendationsService(clock, log).goDown();
        ProductPageService pages = new ProductPageService(down, breakerFor("Recommendations"), log);

        for (int i = 0; i < 10; i++) {
            pages.page(SKU);
        }

        assertEquals(3 * RecommendationsService.TIMEOUT_MILLIS, clock.millis(),
                "three timeouts in total, not ten");
    }

    @Test
    @DisplayName("a working Recommendations gives a page that is not degraded")
    void theHealthyPathIsUnchanged() {
        RecommendationsService up = new RecommendationsService(clock, log);
        ProductPageService pages = new ProductPageService(up, breakerFor("Recommendations"), log);

        ProductPage page = pages.page(SKU);

        assertEquals(2, page.suggestions().size());
        assertEquals(false, page.degraded());
    }

    // -------------------------------------------- essential: refuse, and say so

    @Test
    @DisplayName("checkout refuses honestly rather than falling back")
    void theEssentialDependencyHasNoFallback() {
        PaymentsService down = new PaymentsService(clock, log).goDown();
        CheckoutService checkout = new CheckoutService(down, breakerFor("Payments"), log);

        CheckoutUnavailableException told = assertThrows(CheckoutUnavailableException.class,
                () -> checkout.pay("ORD-5001", AMOUNT));

        assertTrue(told.getMessage().contains("basket is saved"));
        assertEquals(0, down.chargesMade());
    }

    @Test
    @DisplayName("once open, checkout says no in no time at all")
    void anHonestNoIsFast() {
        PaymentsService down = new PaymentsService(clock, log).goDown();
        CheckoutService checkout = new CheckoutService(down, breakerFor("Payments"), log);

        for (int i = 0; i < 3; i++) {
            assertThrows(CheckoutUnavailableException.class, () -> checkout.pay("ORD", AMOUNT));
        }
        long afterTripping = clock.millis();

        assertThrows(CheckoutUnavailableException.class, () -> checkout.pay("ORD", AMOUNT));

        assertEquals(afterTripping, clock.millis(),
                "a spinner for three seconds is not better than a clear message now");
    }

    @Test
    @DisplayName("checkout works normally when payments are healthy")
    void theHealthyCheckoutIsUnchanged() {
        PaymentsService up = new PaymentsService(clock, log);
        CheckoutService checkout = new CheckoutService(up, breakerFor("Payments"), log);

        assertEquals("chg-1", checkout.pay("ORD-5001", AMOUNT));
        assertEquals(1, up.chargesMade());
    }

    // --------------------------------------------- the fallback that must not be

    @Test
    @DisplayName("a lying fallback returns a receipt for money that never moved")
    void aDishonestFallbackHidesTheOutage() {
        PaymentsService down = new PaymentsService(clock, log).goDown();
        PretendItWorkedCheckoutService checkout =
                new PretendItWorkedCheckoutService(down, breakerFor("Payments"), log);

        String receipt = assertDoesNotThrow(() -> checkout.pay("ORD-9001", AMOUNT));

        assertEquals("chg-assumed-ok", receipt);
        assertEquals(0, down.chargesMade(), "the shopper was thanked and charged nothing");
        assertTrue(log.timeline().contains("PRETENDED"),
                "the only trace is a log line nobody is watching");
    }
}
