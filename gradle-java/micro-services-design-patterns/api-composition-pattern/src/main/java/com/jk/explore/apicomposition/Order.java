package com.jk.explore.apicomposition;

import java.util.List;

/**
 * What the Orders service knows: which skus, how many, at what price.
 *
 * It does not know what any of them are called. That is Catalog's data, in Catalog's
 * database, and the reason it is not here is the previous project in this category.
 */
public record Order(String orderId, String customerId, List<Line> lines) {

    /** One line of an order. A sku, a quantity, a price, and no product name. */
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
