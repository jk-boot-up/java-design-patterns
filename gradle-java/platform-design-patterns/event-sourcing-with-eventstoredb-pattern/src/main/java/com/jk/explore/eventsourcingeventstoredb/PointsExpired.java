package com.jk.explore.eventsourcingeventstoredb;

import java.time.LocalDate;

/** Points that were not spent within twelve months ran out. */
public record PointsExpired(String customerId, int points, LocalDate on) implements LoyaltyEvent {

    @Override
    public int effectOnBalance() {
        return -points;
    }

    @Override
    public String because() {
        return "lost " + points + " points to the twelve-month expiry";
    }
}
