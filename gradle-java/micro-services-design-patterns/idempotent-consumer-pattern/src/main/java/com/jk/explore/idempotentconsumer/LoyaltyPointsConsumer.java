package com.jk.explore.idempotentconsumer;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * The counter-example: a handler that adds to a total, which is the commonest way to get this
 * wrong.
 *
 * "Give the customer one point per pound spent" is a perfectly reasonable requirement, and
 * {@code points += ...} is the obvious way to write it. Run it twice and the customer has twice
 * the points. Nothing throws, nothing is logged, and nobody notices until the shop is quietly
 * giving away money.
 *
 * <p>Two ways out, and the second is better.
 *
 * <ul>
 *   <li>Remember the message ids, as {@link IdempotentNotificationConsumer} does. Works, and
 *       costs a table.</li>
 *   <li>Rewrite the operation so that repeating it does nothing: store the points
 *       <em>per order</em> and set them, instead of adding to a running total. Then the total
 *       is a sum over rows, the same message twice sets the same row twice, and there is
 *       nothing to remember. {@link #awardForOrder} is that version.</li>
 * </ul>
 *
 * <p>Reaching for the dedupe store before asking whether the operation can be rewritten is the
 * most common mistake in this whole area.
 */
public final class LoyaltyPointsConsumer implements MessageConsumer {

    private final Map<String, Integer> pointsPerOrder = new LinkedHashMap<>();
    private final CallLog log;

    private int runningTotal;

    public LoyaltyPointsConsumer(CallLog log) {
        this.log = log;
    }

    @Override
    public String name() {
        return "Loyalty";
    }

    /** The obvious version, and the broken one. */
    @Override
    public void handle(Message message) {
        int earned = (int) (message.total().pence() / 100);
        runningTotal += earned;
        log.note(name(), "ADDED", "+" + earned + " points, total now " + runningTotal);
    }

    /** The rewritten version: set the points for this order rather than adding to a total. */
    public void awardForOrder(Message message) {
        int earned = (int) (message.total().pence() / 100);
        pointsPerOrder.put(message.orderId(), earned);
        log.note(name(), "SET", message.orderId() + " -> " + earned + " points, total now "
                + pointsAwarded());
    }

    /** What the running total says. */
    public int runningTotal() {
        return runningTotal;
    }

    /** What the per-order rows add up to. */
    public int pointsAwarded() {
        return pointsPerOrder.values().stream().mapToInt(Integer::intValue).sum();
    }
}
