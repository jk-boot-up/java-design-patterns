package com.jk.explore.mvcspring;

import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * The model: the one place a total is worked out. Ten per cent comes off a basket of
 * three hundred pounds or more. Every view, HTML or JSON, shows what this says.
 */
public record OrderSummary(String orderId, String customer, List<Line> lines, long subtotalPence, long discountPence, long totalPence) {

    /** How many times a summary has been computed, so the demo can show it is once per request. */
    static final AtomicInteger COMPUTATIONS = new AtomicInteger();

    public static OrderSummary of(Order order) {
        COMPUTATIONS.incrementAndGet();
        long subtotal = order.lines().stream().mapToLong(l -> l.quantity() * l.pricePence()).sum();
        long discount = subtotal >= 30000 ? subtotal / 10 : 0;
        return new OrderSummary(order.id(), order.customer(), order.lines(), subtotal, discount, subtotal - discount);
    }

    public String totalDisplay() {
        return pounds(totalPence);
    }

    public String discountDisplay() {
        return pounds(discountPence);
    }

    static String pounds(long pence) {
        return String.format("£%d.%02d", pence / 100, pence % 100);
    }
}
