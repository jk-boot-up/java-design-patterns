package com.jk.explore.markerinterface;

import java.util.List;

/**
 * Without the pattern: care instructions as free-text tags, typed by whoever adds the product.
 */
public record TaggedProduct(String sku, List<String> tags) {

    public String pack() {
        return sku + ": " + (tags.contains("perishable") ? "ice packs" : "plain box");
    }
}
