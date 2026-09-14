package com.jk.explore.circuitbreaker;

import java.util.List;

/**
 * The naive alternative: retry, applied to an outage.
 *
 * This is the previous pattern in the category used in the wrong place, and it is a
 * genuinely easy mistake — retry is the right answer to a failed call often enough
 * that it starts to look like the right answer to every failed call.
 *
 * <p>Against a service that is properly down, three attempts at a three-second
 * timeout means the shopper waits <strong>nine seconds</strong> to be shown a page
 * with no suggestions on it. Worse, every shopper does the same, so a service that
 * is struggling is now receiving three times the traffic it was struggling under.
 *
 * <p>The question that separates the two patterns is worth memorising: <em>is the
 * next attempt plausibly going to work?</em> For a dropped connection, yes — retry.
 * For a service that has failed the last twenty calls, no — break.
 */
public final class RetryingProductPageService {

    private static final int ATTEMPTS = 3;

    private final RecommendationsService recommendations;
    private final CallLog log;

    public RetryingProductPageService(RecommendationsService recommendations, CallLog log) {
        this.recommendations = recommendations;
        this.log = log;
    }

    /** Always returns a page, eventually. */
    public ProductPage page(String sku) {
        for (int attempt = 1; attempt <= ATTEMPTS; attempt++) {
            try {
                return new ProductPage(sku, "Barista Pro Espresso Machine",
                        recommendations.suggestionsFor(sku), false);
            } catch (ServiceUnavailableException e) {
                log.note("ProductPage", "RETRYING", "attempt " + attempt + " timed out");
            }
        }
        return new ProductPage(sku, "Barista Pro Espresso Machine", List.of(), true);
    }
}
