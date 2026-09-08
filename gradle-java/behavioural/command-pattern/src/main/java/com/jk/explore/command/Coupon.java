package com.jk.explore.command;

import java.util.Objects;

/**
 * A discount code and what it takes off.
 *
 * <p>A cart holds at most one of these. That single-slot rule is what makes
 * {@link ApplyCouponCommand}'s undo interesting: applying a coupon to a cart
 * that already had one does not add anything, it <em>replaces</em>
 * something — and undoing it has to put the old one back.
 */
public record Coupon(String code, int percentOff) {

    public Coupon {
        Objects.requireNonNull(code, "code");
        if (code.isBlank()) {
            throw new IllegalArgumentException("a coupon needs a code");
        }
        if (percentOff <= 0 || percentOff > 100) {
            throw new IllegalArgumentException(
                    "percentOff must be between 1 and 100, was " + percentOff);
        }
    }

    /** What this coupon takes off the given subtotal. */
    public Money discountOn(Money subtotal) {
        return subtotal.percent(percentOff);
    }

    @Override
    public String toString() {
        return code + " (-" + percentOff + "%)";
    }
}
