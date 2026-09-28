package com.jk.explore.eventsourcingeventstoredb;

import java.time.LocalDate;

/** The customer earned points on an order. */
public record PointsAwarded(String customerId, int points, String orderId, LocalDate on)
        implements LoyaltyEvent {

    @Override
    public int effectOnBalance() {
        return points;
    }

    @Override
    public String because() {
        return "earned " + points + " points on order " + orderId;
    }

    /** The same award for a different customer. */
    public PointsAwarded withCustomer(String otherCustomer) {
        return new PointsAwarded(otherCustomer, points, orderId, on);
    }
}
