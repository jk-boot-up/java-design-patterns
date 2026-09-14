package com.jk.explore.circuitbreaker;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Retry applied to an outage. Every test passes; the cost is in the numbers.
 *
 * The question that separates the two patterns: is the next attempt plausibly going
 * to work? For a dropped connection, yes. For a service that has failed the last
 * twenty calls, no — and asking it twice more is how a slow shop becomes a dead one.
 */
class RetryingProductPageServiceTest {

    private static final String SKU = "SKU-1234";

    private SimulatedClock clock;
    private CallLog log;

    @BeforeEach
    void setUp() {
        clock = new SimulatedClock();
        log = new CallLog(clock);
    }

    @Test
    @DisplayName("it does serve a page, so nothing looks broken")
    void itStillServesAPage() {
        RecommendationsService down = new RecommendationsService(clock, log).goDown();

        ProductPage page = new RetryingProductPageService(down, log).page(SKU);

        assertEquals("Barista Pro Espresso Machine", page.name());
        assertTrue(page.degraded());
    }

    @Test
    @DisplayName("one page costs the shopper nine seconds")
    void oneShopperWaitsNineSeconds() {
        RecommendationsService down = new RecommendationsService(clock, log).goDown();

        new RetryingProductPageService(down, log).page(SKU);

        assertEquals(9_000, clock.millis());
    }

    @Test
    @DisplayName("it triples the traffic to the service that is already down")
    void itMakesTheOutageWorse() {
        RecommendationsService down = new RecommendationsService(clock, log).goDown();

        new RetryingProductPageService(down, log).page(SKU);

        assertEquals(3, down.callsReceived());
    }

    @Test
    @DisplayName("ten shoppers cost ninety seconds and thirty calls; a breaker costs nine and three")
    void theComparison() {
        RecommendationsService retriedAgainst = new RecommendationsService(clock, log).goDown();
        RetryingProductPageService retrying = new RetryingProductPageService(retriedAgainst, log);
        for (int i = 0; i < 10; i++) {
            retrying.page(SKU);
        }
        long retryTime = clock.millis();

        SimulatedClock brokenClock = new SimulatedClock();
        CallLog brokenLog = new CallLog(brokenClock);
        RecommendationsService brokenAgainst = new RecommendationsService(brokenClock, brokenLog).goDown();
        ProductPageService broken = new ProductPageService(brokenAgainst,
                new CircuitBreaker("Recommendations", 3, 5_000, brokenClock, brokenLog), brokenLog);
        for (int i = 0; i < 10; i++) {
            broken.page(SKU);
        }

        assertEquals(90_000, retryTime);
        assertEquals(30, retriedAgainst.callsReceived());
        assertEquals(9_000, brokenClock.millis());
        assertEquals(3, brokenAgainst.callsReceived());
    }

    @Test
    @DisplayName("when the service is healthy, retrying costs nothing extra")
    void itIsHarmlessWhenNothingIsWrong() {
        RecommendationsService up = new RecommendationsService(clock, log);

        ProductPage page = new RetryingProductPageService(up, log).page(SKU);

        assertEquals(2, page.suggestions().size());
        assertEquals(RecommendationsService.HEALTHY_MILLIS, clock.millis());
    }
}
