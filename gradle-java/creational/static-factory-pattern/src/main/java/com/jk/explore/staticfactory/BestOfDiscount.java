package com.jk.explore.staticfactory;

/**
 * Applies whichever of two discounts is worth more on the order in front of
 * it — so the answer can differ from one order to the next.
 *
 * <p>A caller could not have written this by hand without knowing both of
 * the other classes. Through {@code Discount.bestOf(...)} it never learns
 * any of the three.
 */
final class BestOfDiscount implements Discount {

    private final Discount first;
    private final Discount second;

    BestOfDiscount(Discount first, Discount second) {
        this.first = first;
        this.second = second;
    }

    @Override
    public Money appliedTo(Order order) {
        Money a = first.appliedTo(order);
        Money b = second.appliedTo(order);
        return a.compareTo(b) >= 0 ? a : b;
    }

    @Override
    public String describe() {
        return "Best of: " + first.describe() + " / " + second.describe();
    }
}
