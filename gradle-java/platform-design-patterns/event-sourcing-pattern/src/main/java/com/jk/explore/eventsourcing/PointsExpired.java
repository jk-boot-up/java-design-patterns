package com.jk.explore.eventsourcing;

import java.time.LocalDate;

/**
 * Points the customer never spent, taken back after twelve months.
 *
 * <p>This one is included because expiry is where a current-state row hurts
 * most. A customer rings up asking why their balance dropped overnight when they
 * bought nothing and spent nothing, and the answer is a scheduled job that ran
 * at three in the morning. With a row there is nothing to show them. With a log
 * there is a line, with a date on it, saying exactly that.
 *
 * <p>There is no order id, because nothing the customer did caused this. The
 * shop did it.
 */
public record PointsExpired(String customerId, int points,
                            LocalDate on) implements LoyaltyEvent {

    @Override
    public int effectOnBalance() {
        return -points;
    }

    @Override
    public String because() {
        return "lost " + points + " points to the twelve-month expiry";
    }
}
