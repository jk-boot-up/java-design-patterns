package com.jk.explore.circuitbreaker;

import java.util.List;

/**
 * The product page: a breaker with a fallback, because suggestions are optional.
 *
 * This is the easy half. If Recommendations cannot be reached, the page goes out
 * without suggestions and says so. The shopper still gets to buy the espresso
 * machine, which is the only thing the shop actually needs from this page.
 */
public final class ProductPageService {

    private final RecommendationsService recommendations;
    private final CircuitBreaker breaker;
    private final CallLog log;

    public ProductPageService(RecommendationsService recommendations, CircuitBreaker breaker,
                              CallLog log) {
        this.recommendations = recommendations;
        this.breaker = breaker;
        this.log = log;
    }

    /** Always returns a page. Never throws. */
    public ProductPage page(String sku) {
        try {
            List<String> suggestions = breaker.call(() -> recommendations.suggestionsFor(sku));
            return new ProductPage(sku, "Barista Pro Espresso Machine", suggestions, false);
        } catch (CircuitOpenException refused) {
            // The cheap case: no call was made, so this cost nothing at all.
            log.note("ProductPage", "DEGRADED", "page served without suggestions, no call made");
            return new ProductPage(sku, "Barista Pro Espresso Machine", List.of(), true);
        } catch (ServiceUnavailableException failed) {
            // The expensive case: three seconds went by before we learned this.
            log.note("ProductPage", "DEGRADED", "page served without suggestions after a timeout");
            return new ProductPage(sku, "Barista Pro Espresso Machine", List.of(), true);
        }
    }
}
