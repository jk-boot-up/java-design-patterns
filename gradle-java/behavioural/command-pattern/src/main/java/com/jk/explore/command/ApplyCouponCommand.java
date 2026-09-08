package com.jk.explore.command;

import java.util.Objects;

/**
 * Puts a discount code on the cart.
 *
 * <p>A cart holds at most one coupon, so applying a second one does not add
 * anything — it replaces the first. That makes undo "restore whatever was
 * there before", which is very often nothing, and occasionally a different
 * coupon. Undoing by clearing the coupon would be correct nine times out of
 * ten and silently wrong the tenth: the customer would lose a discount they
 * never touched.
 */
public final class ApplyCouponCommand implements CartCommand {

    private final Coupon coupon;

    /** Null both before execution and when there genuinely was no coupon. */
    private Coupon previousCoupon;
    private boolean executed;

    public ApplyCouponCommand(Coupon coupon) {
        this.coupon = Objects.requireNonNull(coupon, "coupon");
    }

    @Override
    public String describe() {
        return "apply coupon " + coupon.code();
    }

    @Override
    public void execute(Cart cart) {
        previousCoupon = cart.coupon().orElse(null);
        cart.setCoupon(coupon);
        executed = true;
    }

    @Override
    public void undo(Cart cart) {
        if (!executed) {
            throw new IllegalStateException("cannot undo a command that has not run: " + describe());
        }
        cart.setCoupon(previousCoupon);
    }
}
