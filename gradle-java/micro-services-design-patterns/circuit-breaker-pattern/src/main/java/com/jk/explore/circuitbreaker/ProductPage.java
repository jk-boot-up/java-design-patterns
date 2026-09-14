package com.jk.explore.circuitbreaker;

import java.util.List;

/**
 * A product page, with or without its suggestions.
 *
 * {@code degraded} is not decoration. It is the page admitting that something was
 * left out, which is what makes the fallback honest — the shop knows, the monitoring
 * knows, and nobody has to guess later whether an empty suggestion list meant "we
 * had none" or "Recommendations was down".
 */
public record ProductPage(String sku, String name, List<String> suggestions, boolean degraded) {

    public String summary() {
        return name + ", " + suggestions.size() + " suggestion(s)"
                + (degraded ? " (Recommendations left out)" : "");
    }
}
