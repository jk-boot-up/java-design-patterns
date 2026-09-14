package com.jk.explore.apigateway;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * What only the gateway gives you.
 *
 * A correct product page is not evidence of anything — the naive app produces
 * one too. So none of these tests is happy about the page. They are about the
 * number of network crossings, the number of token checks, and which failures
 * are allowed to reach the shopper.
 */
class ProductPageGatewayTest {

    private static final String SKU = "SKU-1234";

    private SimulatedClock clock;
    private CallLog log;
    private AuthService auth;
    private StoreServices services;
    private ProductPageGateway gateway;

    @BeforeEach
    void setUp() {
        clock = new SimulatedClock();
        log = new CallLog(clock);
        auth = new AuthService();
        services = StoreServices.onInternalNetwork(clock, log);
        gateway = new ProductPageGateway(auth, services, log);
    }

    private MobileApp app() {
        return new MobileApp(gateway, AuthService.validToken(), clock, log);
    }

    @Test
    void theAppCrossesTheMobileNetworkExactlyOnce() {
        MobileApp app = app();

        app.productPage(SKU);

        assertEquals(1, app.remoteCalls(),
                "the whole point: one call from the phone, not four");
    }

    @Test
    void theTokenIsCheckedOnceAtTheEdgeRatherThanOncePerService() {
        app().productPage(SKU);

        assertEquals(1, auth.checks(),
                "the gateway authenticates once and the services behind it trust it");
    }

    @Test
    void theGatewayCallsAllFourServicesToBuildOnePage() {
        app().productPage(SKU);

        assertEquals(1, services.catalog().invocations());
        assertEquals(1, services.pricing().invocations());
        assertEquals(1, services.inventory().invocations());
        assertEquals(1, services.recommendations().invocations());
    }

    @Test
    void theFourInternalCallsHappenInsideTheOneMobileCall() {
        app().productPage(SKU);

        assertEquals(
                java.util.List.of("Gateway", "Gateway", "Catalog", "Pricing",
                        "Inventory", "Recommendations"),
                log.services(),
                "the gateway's own call opens the timeline; everything else is nested in it");
    }

    @Test
    void theShopperWaitsForOneSlowTripPlusFourFastOnes() {
        app().productPage(SKU);

        // 200ms out and back to the gateway, with four 10ms internal calls
        // happening inside that trip.
        assertEquals(240, log.elapsedMillis());
    }

    @Test
    void thatIsMoreThanThreeTimesFasterThanCallingTheServicesDirectly() {
        SimulatedClock naiveClock = new SimulatedClock();
        CallLog naiveLog = new CallLog(naiveClock);
        new NaiveMobileApp(new AuthService(),
                StoreServices.onMobileNetwork(naiveClock, naiveLog),
                AuthService.validToken()).productPage(SKU);

        app().productPage(SKU);

        assertEquals(800, naiveLog.elapsedMillis(), "four trips at 200ms each");
        assertTrue(log.elapsedMillis() * 3 < naiveLog.elapsedMillis(),
                "240ms against 800ms");
    }

    @Test
    void anOptionalServiceFailingStillProducesAPage() {
        services.recommendations().failNext(1);

        ProductPage page = app().productPage(SKU);

        assertEquals("Barista Pro Espresso Machine", page.name());
        assertEquals(Money.pence(44999), page.price());
        assertTrue(page.inStock());
        assertTrue(page.recommendedSkus().isEmpty());
        assertTrue(page.isDegraded());
    }

    @Test
    void theDegradedPageIsRecordedSoSomebodyCanSeeItHappened() {
        services.recommendations().failNext(1);

        app().productPage(SKU);

        assertTrue(log.entries().stream()
                        .anyMatch(e -> "DEGRADED".equals(e.outcome())),
                "serving a page without suggestions is a decision, and it is logged");
    }

    @Test
    void aServiceThePageCannotDoWithoutIsAllowedToFailTheWholeCall() {
        services.pricing().failNext(1);

        ServiceUnavailableException failure = assertThrows(ServiceUnavailableException.class,
                () -> app().productPage(SKU));

        assertEquals("Pricing", failure.serviceName(),
                "a page with no price on it is worse than an honest error");
    }

    @Test
    void theGatewayStopsAtTheFirstEssentialFailureRatherThanFinishingThePage() {
        services.catalog().failNext(1);

        assertThrows(ServiceUnavailableException.class, () -> app().productPage(SKU));

        assertEquals(0, services.pricing().invocations(),
                "no point pricing a product whose name could not be fetched");
    }

    @Test
    void anUnknownTokenIsRejectedBeforeAnyServiceIsCalled() {
        MobileApp signedOut = new MobileApp(gateway, "tok-forged", clock, log);

        assertThrows(IllegalArgumentException.class, () -> signedOut.productPage(SKU));

        assertEquals(0, services.catalog().invocations(),
                "authentication happens at the edge, so a forged token costs the "
                        + "services nothing");
    }

    @Test
    void aProductWithNoStockIsAPageNotAnError() {
        ProductPage page = app().productPage("SKU-2002");

        assertFalse(page.inStock());
        assertEquals("Stainless Milk Jug", page.name());
    }

    @Test
    void theGatewayMakesNoPricingDecisionsOfItsOwn() {
        ProductPage page = app().productPage(SKU);

        assertEquals(new PricingService().price(SKU), page.price(),
                "the price on the page is Pricing's answer, unmodified. A gateway "
                        + "that discounts is a gateway that owns business rules.");
    }

    @Test
    void theAppNeverLearnsWhichServicesExist() {
        long publicMethods = java.util.Arrays.stream(MobileApp.class.getDeclaredMethods())
                .filter(m -> java.lang.reflect.Modifier.isPublic(m.getModifiers()))
                .count();

        assertEquals(2, publicMethods,
                "productPage and a call counter. No service addresses, no response "
                        + "shapes, nothing that changes when a service moves.");
    }
}
