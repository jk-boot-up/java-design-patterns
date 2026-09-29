package com.jk.explore.processcamel;

/**
 * An order for one item, paid with one card.
 */
public record Order(String id, String sku, String card) {
}
