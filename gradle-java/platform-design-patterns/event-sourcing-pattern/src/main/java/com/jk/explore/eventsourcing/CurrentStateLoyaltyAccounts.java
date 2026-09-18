package com.jk.explore.eventsourcing;

import java.time.LocalDate;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Set;

/**
 * The naive version: one number per customer, overwritten in place.
 *
 * <p>This is how almost every loyalty scheme is built, and it is worth saying
 * plainly that it is not stupid. It is small, it is fast, the balance is one
 * lookup away, and for a shop whose customers never ask questions it is the right
 * answer. This project is not an argument against it in general.
 *
 * <p>What it cannot do is answer <em>why</em>. Look at {@link #award}: the new
 * balance is written over the old one, and at that instant the fact that a
 * hundred and twenty points arrived on the eighth of March stops existing
 * anywhere in the shop. Nothing was corrupted and no bug was involved — the
 * information was simply never kept.
 *
 * <p>And that is also why this design cannot survive its own bugs. When a
 * release awards points twice, the second award lands on the row exactly like the
 * first one did, and afterwards there is no trace of there having been two. The
 * evidence you would need to find the affected customers was overwritten by the
 * very thing that went wrong.
 */
public final class CurrentStateLoyaltyAccounts implements LoyaltyAccounts {

    private final Map<String, Integer> points = new LinkedHashMap<>();

    @Override
    public void award(String customerId, int amount, String orderId, LocalDate on) {
        // orderId and on are accepted and then dropped. Nothing is wrong with
        // this code; the loss is in the design, and it happens on this line.
        points.merge(customerId, amount, Integer::sum);
    }

    @Override
    public void redeem(String customerId, int amount, String orderId, LocalDate on) {
        points.merge(customerId, -amount, Integer::sum);
    }

    @Override
    public void expire(String customerId, int amount, LocalDate on) {
        points.merge(customerId, -amount, Integer::sum);
    }

    @Override
    public int balanceFor(String customerId) {
        return points.getOrDefault(customerId, 0);
    }

    /** Every customer with a row, in the order they first appeared. */
    public Set<String> customers() {
        return points.keySet();
    }

    /**
     * The best answer this design can give support, which is not an answer.
     *
     * <p>It is one sentence long because there is only one sentence available.
     * The row knows the total and nothing else, so "why is it 140" becomes "it is
     * 140".
     */
    public String explain(String customerId) {
        return "the row says " + balanceFor(customerId)
                + " points. How it got there was never written down.";
    }
}
