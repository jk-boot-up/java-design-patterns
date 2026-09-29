package com.jk.explore.money;

import java.util.ArrayList;
import java.util.List;

/**
 * The same cart, with every price held as Money in one currency.
 *
 * <p>It adds lines, and it spreads a basket discount across the lines so that
 * each line's share is known and the shares add up to the whole discount.
 */
public final class Cart {

    /** One line of the cart: what it is, the price of one, and how many. */
    public record Line(String item, Money unitPrice, int quantity) {
        public Money total() {
            return unitPrice.times(quantity);
        }
    }

    private final Currency currency;
    private final List<Line> lines = new ArrayList<>();

    public Cart(Currency currency) {
        this.currency = currency;
    }

    public Cart add(String item, Money unitPrice, int quantity) {
        if (unitPrice.currency() != currency) {
            throw new IllegalArgumentException("this cart is in " + currency + ", not " + unitPrice.currency());
        }
        lines.add(new Line(item, unitPrice, quantity));
        return this;
    }

    public List<Line> lines() {
        return List.copyOf(lines);
    }

    public Money total() {
        Money total = Money.zero(currency);
        for (Line line : lines) {
            total = total.plus(line.total());
        }
        return total;
    }

    /** Each line's share of a basket discount, in proportion to the line's total. */
    public Money[] discountShares(Money discount) {
        long[] weights = new long[lines.size()];
        for (int i = 0; i < weights.length; i++) {
            weights[i] = lines.get(i).total().minor();
        }
        return discount.allocate(weights);
    }
}
