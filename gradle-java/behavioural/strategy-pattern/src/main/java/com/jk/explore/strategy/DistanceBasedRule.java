package com.jk.explore.strategy;

import java.util.Objects;

/**
 * A base fee plus a charge for every hundred miles, part-hundreds rounded up.
 *
 * <p>Rounding up is the interesting decision here, and it is the sort of thing
 * that gets lost when four rules share one method: 101 miles costs the same as
 * 200. Alone in its own class, with its own test, it is visible and
 * deliberate.
 */
public final class DistanceBasedRule implements ShippingCostRule {

    private static final int MILES_PER_UNIT = 100;

    private final Money baseFee;
    private final Money perHundredMiles;

    public DistanceBasedRule(Money baseFee, Money perHundredMiles) {
        this.baseFee = Objects.requireNonNull(baseFee, "baseFee");
        this.perHundredMiles = Objects.requireNonNull(perHundredMiles, "perHundredMiles");
    }

    /** The store's standard distance pricing: £2.00 plus £1.50 per 100 miles. */
    public static DistanceBasedRule standard() {
        return new DistanceBasedRule(Money.pounds(2.00), Money.pounds(1.50));
    }

    @Override
    public String name() {
        return "Distance based";
    }

    @Override
    public Money costFor(Shipment shipment) {
        int units = (shipment.distanceMiles() + MILES_PER_UNIT - 1) / MILES_PER_UNIT;
        Money cost = baseFee;
        for (int i = 0; i < units; i++) {
            cost = cost.plus(perHundredMiles);
        }
        return cost;
    }
}
