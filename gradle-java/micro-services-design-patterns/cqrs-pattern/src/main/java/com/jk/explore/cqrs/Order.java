package com.jk.explore.cqrs;

import java.util.List;

/**
 * The write side's order: normalised, and deliberately dull.
 *
 * There is no product name here and no delivery status, because this shape exists to be
 * changed correctly rather than to be displayed. Every fact appears exactly once, which
 * is what makes it safe to update and awkward to read.
 */
public record Order(String orderId, String customerId, List<Line> lines,
                    long placedAtMillis) {

    /** One line: a sku, a quantity, a price. */
    public record Line(String sku, int quantity, Money unitPrice) {

        public Money lineTotal() {
            return unitPrice.times(quantity);
        }
    }

    public Money total() {
        return lines.stream().map(Line::lineTotal).reduce(Money.pence(0), Money::plus);
    }

    public List<String> skus() {
        return lines.stream().map(Line::sku).distinct().toList();
    }
}
