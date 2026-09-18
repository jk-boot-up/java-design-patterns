package com.jk.explore.hexagonal.core.domain;

/**
 * One line of an order: what was bought, how many, and what that came to.
 *
 * <p>The line total is stored rather than recalculated on demand, because a
 * price can change after an order is placed and the customer was charged the
 * old one.
 */
public record OrderLine(String sku, int quantity, Money lineTotal) {

    public static OrderLine of(Product product, int quantity) {
        return new OrderLine(product.sku(), quantity, product.price().times(quantity));
    }
}
