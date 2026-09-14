package com.jk.explore.apigateway;

import java.util.List;
import java.util.Map;

/**
 * The Recommendations service: "customers also bought".
 *
 * This service is <strong>optional</strong>, and that single fact does more
 * teaching in this category than any other. A product page with no suggestions
 * on it is a perfectly good product page. A product page with no price is not.
 * Every decision about what to do when a call fails comes back to which kind of
 * service failed.
 */
public final class RecommendationsService {

    private final Map<String, List<String>> alsoBought = Map.of(
            "SKU-1234", List.of("SKU-2001", "SKU-2002"),
            "SKU-2001", List.of("SKU-1234"),
            "SKU-2002", List.of("SKU-1234"));

    public List<String> alsoBought(String sku) {
        return alsoBought.getOrDefault(sku, List.of());
    }
}
