package com.jk.explore.eventsourcing;

import java.time.LocalDate;

/**
 * The part of the shop that awards points, and the part that gets it wrong.
 *
 * <p>One point per pound spent. A ninety-pound order earns ninety points, which
 * keeps the arithmetic in this project something a listener can follow without
 * writing anything down.
 *
 * <p>{@link #shipTheDoubleAwardingRelease()} is the bug, and it is the smallest
 * bug that could possibly cause this much trouble: the award line ends up running
 * twice. In real life it arrives as a retry that was not idempotent, or a listener
 * registered twice at startup, or a merge that duplicated four lines. The cause
 * does not matter. What matters is that it is live for a while before anybody
 * notices, and then somebody has to work out who was affected.
 *
 * <p>The checkout does not know which kind of store it is talking to — it holds a
 * {@link LoyaltyAccounts}. That is the point: the bug is identical in both
 * worlds, and only the ability to investigate it afterwards differs.
 */
public final class Checkout {

    private final LoyaltyAccounts accounts;
    private boolean awardingTwice;

    public Checkout(LoyaltyAccounts accounts) {
        this.accounts = accounts;
    }

    /** The bad release goes out. Nobody notices for three weeks. */
    public void shipTheDoubleAwardingRelease() {
        awardingTwice = true;
    }

    /** The fix goes out. It stops new damage and undoes none of the old. */
    public void shipTheFix() {
        awardingTwice = false;
    }

    /** An order is placed, and the customer earns a point per pound. */
    public void placeOrder(String customerId, String orderId, int pounds, LocalDate on) {
        accounts.award(customerId, pounds, orderId, on);
        if (awardingTwice) {
            accounts.award(customerId, pounds, orderId, on);
        }
    }
}
