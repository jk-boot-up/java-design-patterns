package com.jk.explore.externalisedconfig;

/**
 * The checkout a competent developer writes on the first day: correct, clear,
 * and impossible to change without a release.
 *
 * <p>Look at {@link #FREE_DELIVERY_OVER}. There is nothing wrong with it. It is
 * a named constant rather than a bare number, it says what it means, it is in
 * one place, and a code reviewer would pass it without comment. If anyone tells
 * you this class is badly written they have missed the problem, because the
 * problem is not in the code at all.
 *
 * <p>The problem is in the <em>lifecycle</em>. This number is now part of the
 * compiled program, which means the only way to change it is to compile a new
 * program: edit, review, build, test, approve, deploy. That path exists for
 * good reasons and it is exactly what you want in front of a change to how the
 * total is calculated. It is absurd in front of a change from fifty to
 * thirty-five, and it is worse than absurd when the new value has to be live at
 * nine o'clock on a Saturday morning. See {@link ReleasePipeline} for what that
 * path actually costs in hours.
 */
public final class HardCodedCheckout implements Checkout {

    /**
     * Spend this much, or more, and delivery is free.
     *
     * <p>This is the line the whole project is about. It is a good line. It is
     * also, right now, a decision that only a software release can revisit.
     */
    private static final Money FREE_DELIVERY_OVER = Money.pounds(50);

    /** What delivery costs when the basket is under the threshold. */
    private static final Money STANDARD_DELIVERY = Money.pence(499);

    @Override
    public DeliveryQuote quote(Basket basket) {
        Money cost = basket.goodsTotal().isAtLeast(FREE_DELIVERY_OVER)
                ? Money.zero()
                : STANDARD_DELIVERY;
        return new DeliveryQuote(basket, cost, FREE_DELIVERY_OVER,
                "a constant compiled into the program");
    }

    @Override
    public String describe() {
        return "HardCodedCheckout, threshold " + FREE_DELIVERY_OVER + " fixed at compile time";
    }

    /**
     * The threshold, exposed only so the tests and the demo can print the
     * number they are talking about rather than repeat it.
     */
    public static Money threshold() {
        return FREE_DELIVERY_OVER;
    }

    /** The standard delivery charge, for the same reason. */
    public static Money standardDelivery() {
        return STANDARD_DELIVERY;
    }
}
