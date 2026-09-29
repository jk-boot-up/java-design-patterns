package com.jk.explore.domainservice;

import java.util.List;

/**
 * The domain objects the pricing rule needs. Each keeps the facts that are its own.
 */
public final class Model {

    public enum Tier { STANDARD, GOLD }

    public record Customer(String id, Tier tier) {
    }

    public record Line(String item, long pricePence) {
    }

    /** The basket knows its own subtotal: that fact belongs to it, not to any service. */
    public record Basket(List<Line> lines) {
        public long subtotalPence() {
            return lines.stream().mapToLong(Line::pricePence).sum();
        }
    }

    /** £5 off baskets over £40. */
    public record Coupon(String code, long offPence, long minimumPence) {
        public static final Coupon SAVE5 = new Coupon("SAVE5", 500, 4000);
    }

    private Model() {
    }
}
