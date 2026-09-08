package com.jk.explore.chain;

import java.util.List;

/**
 * One attempt to check out: everything the checks are allowed to look at, and
 * nothing they are allowed to change.
 *
 * <p>Amounts are whole pounds, kept as {@code int}. A real shop would use a
 * proper money type; here it would only be one more class to learn before
 * reaching the pattern.
 *
 * @param fraudScore 0 (nothing suspicious) to 100 (certainly fraud)
 */
public record CheckoutRequest(String reference,
                              List<BasketItem> items,
                              String country,
                              String postcode,
                              int cardLimitPounds,
                              int fraudScore) {

    public CheckoutRequest {
        items = List.copyOf(items);
    }

    /** What the basket comes to, in pounds. */
    public int totalPounds() {
        return items.stream().mapToInt(BasketItem::totalPounds).sum();
    }

    @Override
    public String toString() {
        return String.format("%-7s £%-6d %-4s %-8s card limit £%-6d fraud %d",
                reference, totalPounds(), country, postcode, cardLimitPounds, fraudScore);
    }
}
