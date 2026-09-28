package com.jk.explore.eventsourcingeventstoredb;

import java.util.List;

/**
 * Adds events up. This is the whole of "working out the current state" in event sourcing:
 * start at zero, and let every event move the number, oldest first.
 */
public final class Balance {

    private Balance() {
    }

    public static int of(List<LoyaltyEvent> events) {
        int balance = 0;
        for (LoyaltyEvent event : events) {
            balance += event.effectOnBalance();
        }
        return balance;
    }
}
