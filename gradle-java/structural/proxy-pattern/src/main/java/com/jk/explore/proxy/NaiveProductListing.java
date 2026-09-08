package com.jk.explore.proxy;

import java.util.ArrayList;
import java.util.List;

/**
 * The trap, kept for contrast: without a virtual proxy, a category page has
 * no choice but to construct every {@link HighResolutionProductImage} up
 * front, including the fifty-odd below the fold that the shopper never
 * scrolls to. Sixty listings means sixty expensive loads before the first
 * pixel is painted, however few are actually seen.
 */
public final class NaiveProductListing {

    private final List<HighResolutionProductImage> images = new ArrayList<>();

    public NaiveProductListing(List<String> skus) {
        for (String sku : skus) {
            images.add(new HighResolutionProductImage(sku));
        }
    }

    public String renderFirst() {
        return images.get(0).render();
    }
}
