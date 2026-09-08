package com.jk.explore.strategy;

import java.util.List;
import java.util.Objects;

/**
 * Prices by weight, in bands: up to 1 kg, up to 5 kg, up to 20 kg, and
 * anything heavier.
 *
 * <p>The bands are data, not code, so a pricing change is a change to the
 * list rather than to the algorithm. This is the rule that most obviously
 * earns its own class: the band table and the lookup that walks it are
 * genuinely something, and inside a {@code switch} in a shared method they
 * would be somebody else's problem to read past.
 */
public final class WeightBandedRule implements ShippingCostRule {

    /** An upper weight limit, inclusive, and what a parcel at or under it costs. */
    public record Band(double upToKg, Money cost) {
        public Band {
            Objects.requireNonNull(cost, "cost");
            if (upToKg <= 0) {
                throw new IllegalArgumentException("band limit must be positive, got " + upToKg);
            }
        }
    }

    /** The store's standard table. Bands must be listed lightest first. */
    public static final List<Band> STANDARD_BANDS = List.of(
            new Band(1, Money.pounds(3.50)),
            new Band(5, Money.pounds(6.00)),
            new Band(20, Money.pounds(12.00)));

    private final List<Band> bands;
    private final Money overweightCost;

    public WeightBandedRule(List<Band> bands, Money overweightCost) {
        Objects.requireNonNull(bands, "bands");
        if (bands.isEmpty()) {
            throw new IllegalArgumentException("at least one band is required");
        }
        this.bands = List.copyOf(bands);
        this.overweightCost = Objects.requireNonNull(overweightCost, "overweightCost");
    }

    /** The store's standard bands, with £25.00 for anything over the heaviest. */
    public static WeightBandedRule standard() {
        return new WeightBandedRule(STANDARD_BANDS, Money.pounds(25.00));
    }

    @Override
    public String name() {
        return "Weight banded";
    }

    @Override
    public Money costFor(Shipment shipment) {
        for (Band band : bands) {
            if (shipment.weightKg() <= band.upToKg()) {
                return band.cost();
            }
        }
        return overweightCost;
    }
}
