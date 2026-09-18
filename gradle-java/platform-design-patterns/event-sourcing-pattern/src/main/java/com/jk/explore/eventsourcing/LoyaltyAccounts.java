package com.jk.explore.eventsourcing;

import java.time.LocalDate;

/**
 * What the rest of the shop asks of loyalty points.
 *
 * <p>Both versions in this project implement this interface, and that is
 * deliberate: the checkout that awards the points cannot tell which one it is
 * talking to. Event sourcing is a decision about what the store keeps, not a
 * change to the code that calls it, and the strongest way to say so is to make
 * the two interchangeable and then let them behave differently when somebody
 * asks a question neither was asked before.
 */
public interface LoyaltyAccounts {

    /** The customer earned points on an order. */
    void award(String customerId, int points, String orderId, LocalDate on);

    /** The customer spent points on an order. */
    void redeem(String customerId, int points, String orderId, LocalDate on);

    /** The twelve-month expiry took points back. */
    void expire(String customerId, int points, LocalDate on);

    /** The balance as it stands now. */
    int balanceFor(String customerId);
}
