package com.jk.explore.apigateway;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

/**
 * The version without a gateway, and its costs pinned so they cannot be
 * argued about.
 *
 * These tests pass. The naive app is not broken; it returns the right page. What
 * these tests record is what it costs, and one thing it gets outright wrong.
 */
class NaiveMobileAppTest {

    private static final String SKU = "SKU-1234";

    private CallLog log;
    private AuthService auth;
    private StoreServices services;
    private NaiveMobileApp app;

    @BeforeEach
    void setUp() {
        SimulatedClock clock = new SimulatedClock();
        log = new CallLog(clock);
        auth = new AuthService();
        services = StoreServices.onMobileNetwork(clock, log);
        app = new NaiveMobileApp(auth, services, AuthService.validToken());
    }

    @Test
    void itDoesProduceTheRightPage() {
        ProductPage page = app.productPage(SKU);

        assertEquals("Barista Pro Espresso Machine", page.name());
        assertEquals(Money.pence(44999), page.price());
        assertEquals(2, page.recommendedSkus().size());
    }

    @Test
    void andItCrossesTheSlowNetworkFourTimesToDoIt() {
        app.productPage(SKU);

        assertEquals(4, log.size());
        assertEquals(800, log.elapsedMillis(),
                "four two-hundred-millisecond round trips, one after another");
    }

    @Test
    void andItChecksTheSameTokenFourTimes() {
        app.productPage(SKU);

        assertEquals(4, auth.checks(),
                "every service insists, and the client has nowhere to put that "
                        + "logic except at each call site");
    }

    @Test
    void andAnOptionalServiceGoingDownCostsTheShopperThePrice() {
        services.recommendations().failNext(1);

        assertThrows(ServiceUnavailableException.class, () -> app.productPage(SKU));

        // This is the bug, and it is a design bug rather than a coding one. The
        // name, the price and the stock level all arrived successfully and were
        // discarded, because the client had no way to say that one of its four
        // dependencies did not matter.
        assertEquals(3, log.entries().stream()
                        .filter(e -> "OK".equals(e.outcome())).count(),
                "three answers arrived and were thrown away with the error");
    }
}
