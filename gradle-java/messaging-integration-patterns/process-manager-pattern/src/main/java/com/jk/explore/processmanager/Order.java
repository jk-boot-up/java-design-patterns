package com.jk.explore.processmanager;

/**
 * An order to fulfil: which product, and which card to charge.
 */
public record Order(String id, String sku, String card) {
}
