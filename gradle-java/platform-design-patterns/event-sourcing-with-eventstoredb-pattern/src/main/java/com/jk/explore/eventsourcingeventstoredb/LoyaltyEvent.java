package com.jk.explore.eventsourcingeventstoredb;

import java.time.LocalDate;

/**
 * One thing that happened to a customer's loyalty points. The shop gives one point per pound
 * spent, lets customers spend points on later orders, and expires unused points.
 *
 * <p>An event is a fact in the past tense. It is never changed after it is written, and
 * nothing about it is stored anywhere else: a balance is always worked out by adding events up.
 */
public sealed interface LoyaltyEvent permits PointsAwarded, PointsRedeemed, PointsExpired {

    String customerId();

    int points();

    LocalDate on();

    /** How this event moves the balance: up for an award, down for a redemption or an expiry. */
    int effectOnBalance();

    /** The event describing itself, for a statement a customer could read. */
    String because();
}
