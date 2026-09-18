package com.jk.explore.eventsourcing;

import java.time.LocalDate;

/**
 * The customer spent points against an order, so the balance goes down.
 *
 * <p>Note what this event does not do: it does not say what the balance became.
 * No event in this project does. An event records the change it made and nothing
 * about the state around it, because the moment an event carries a balance you
 * have two answers that can disagree — the one written into the event and the
 * one you get by adding the events up.
 */
public record PointsRedeemed(String customerId, int points, String orderId,
                             LocalDate on) implements LoyaltyEvent {

    @Override
    public int effectOnBalance() {
        return -points;
    }

    @Override
    public String because() {
        return "spent " + points + " points on order " + orderId;
    }
}
