package com.jk.explore.eventsourcing;

import java.time.LocalDate;

/**
 * One thing that happened to a customer's loyalty points.
 *
 * <p>Read the tense. An event is named in the past — {@code PointsAwarded}, not
 * {@code AwardPoints} — because it is a record of something that already
 * happened, and you cannot argue with it or reject it. That is the difference
 * between an event and a command, and getting the names right is most of
 * getting event sourcing right.
 *
 * <p>An event is also <em>complete on its own</em>. It carries the customer it
 * happened to, the day it happened, how many points it moved, and why. Nothing
 * reading it later has to look anything up to understand it, because there may
 * not be anything left to look up: the order it refers to could have been
 * archived years ago and this event still has to make sense.
 *
 * <p>{@link #effectOnBalance()} is what makes the balance calculation a single
 * line. Awarding fifty points is {@code +50}, redeeming twenty is {@code -20},
 * and the balance is the sum of every effect in order. There is no other
 * arithmetic anywhere in this project.
 */
public sealed interface LoyaltyEvent
        permits PointsAwarded, PointsRedeemed, PointsExpired {

    /** The customer this happened to. */
    String customerId();

    /** The day it happened. Fixed at the time; nothing rewrites it later. */
    LocalDate on();

    /** How many points this moved the balance by, signed. */
    int effectOnBalance();

    /** The same fact in a sentence, for the explanation support reads out. */
    String because();
}
