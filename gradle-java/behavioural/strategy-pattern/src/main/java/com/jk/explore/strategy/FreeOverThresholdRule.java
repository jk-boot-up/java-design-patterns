package com.jk.explore.strategy;

import java.util.Objects;

/**
 * Free delivery once the order is large enough; a fixed fee below that.
 *
 * <p>This is the campaign rule — "free shipping over fifty pounds" — and it is
 * the one that shows why {@link Shipment} carries the order subtotal. Weight
 * and distance say nothing about whether this rule applies; the value of the
 * basket does.
 *
 * <p>Note what it is <em>not</em>: it does not wrap another rule and fall back
 * to it. The fallback is a fixed amount it owns. A rule that delegated to a
 * second rule would be a decorator, and the point of this project is that the
 * four rules are peers, chosen between rather than stacked.
 */
public final class FreeOverThresholdRule implements ShippingCostRule {

    private final Money threshold;
    private final Money feeBelowThreshold;

    public FreeOverThresholdRule(Money threshold, Money feeBelowThreshold) {
        this.threshold = Objects.requireNonNull(threshold, "threshold");
        this.feeBelowThreshold = Objects.requireNonNull(feeBelowThreshold, "feeBelowThreshold");
    }

    /** The current campaign: free over £50.00, otherwise £4.99. */
    public static FreeOverThresholdRule standard() {
        return new FreeOverThresholdRule(Money.pounds(50.00), Money.pounds(4.99));
    }

    @Override
    public String name() {
        return "Free over " + threshold;
    }

    @Override
    public Money costFor(Shipment shipment) {
        return shipment.orderSubtotal().compareTo(threshold) >= 0
                ? Money.zero()
                : feeBelowThreshold;
    }
}
