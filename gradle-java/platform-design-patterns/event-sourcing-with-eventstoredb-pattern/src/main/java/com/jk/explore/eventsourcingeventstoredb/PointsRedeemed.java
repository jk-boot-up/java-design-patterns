package com.jk.explore.eventsourcingeventstoredb;

import java.time.LocalDate;

/** The customer spent points against an order. */
public record PointsRedeemed(String customerId, int points, String orderId, LocalDate on)
        implements LoyaltyEvent {

    @Override
    public int effectOnBalance() {
        return -points;
    }

    @Override
    public String because() {
        return "spent " + points + " points on order " + orderId;
    }
}
