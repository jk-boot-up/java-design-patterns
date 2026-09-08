package com.jk.explore.strategy;

import java.util.Objects;

/**
 * Everything a shipping rule is allowed to look at when it prices a delivery.
 *
 * <p>This type is what makes the rules interchangeable. Every rule takes one
 * of these and returns a {@link Money}, so a rule that needs the weight and a
 * rule that needs the distance have the same signature and the caller cannot
 * tell them apart. If one rule needed an extra argument the others did not,
 * they would stop being substitutable and the pattern would not apply.
 *
 * <p>It carries more than any single rule uses, which is deliberate: the flat
 * rate ignores all of it, the weight bands read only {@code weightKg}, and the
 * distance rule reads only {@code distanceMiles}. A rule taking exactly what
 * it needs would be a tidier method and a useless strategy.
 */
public record Shipment(String destination,
                       double weightKg,
                       int distanceMiles,
                       Money orderSubtotal) {

    public Shipment {
        Objects.requireNonNull(destination, "destination");
        Objects.requireNonNull(orderSubtotal, "orderSubtotal");
        if (destination.isBlank()) {
            throw new IllegalArgumentException("destination must not be blank");
        }
        if (weightKg <= 0) {
            throw new IllegalArgumentException("weight must be positive, got " + weightKg);
        }
        if (distanceMiles < 0) {
            throw new IllegalArgumentException("distance must not be negative, got " + distanceMiles);
        }
    }

    @Override
    public String toString() {
        return String.format("%s, %.1fkg, %d miles, order %s",
                destination, weightKg, distanceMiles, orderSubtotal);
    }
}
