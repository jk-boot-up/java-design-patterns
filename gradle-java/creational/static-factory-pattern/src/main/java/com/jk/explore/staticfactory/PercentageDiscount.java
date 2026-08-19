package com.jk.explore.staticfactory;

/** A percentage off the subtotal. Reachable only via {@code Discount.percentage(int)}. */
final class PercentageDiscount implements Discount {

    private final int percent;

    PercentageDiscount(int percent) {
        this.percent = percent;
    }

    @Override
    public Money appliedTo(Order order) {
        return order.subtotal().percent(percent);
    }

    @Override
    public String describe() {
        return percent + "% off";
    }
}
