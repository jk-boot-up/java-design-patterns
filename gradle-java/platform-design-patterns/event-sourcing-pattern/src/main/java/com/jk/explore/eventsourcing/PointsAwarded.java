package com.jk.explore.eventsourcing;

import java.time.LocalDate;

/**
 * The customer earned points, on an order, on a day. One point per pound spent.
 *
 * <p>This record also carries the project's unhappiest lesson, and it is worth
 * meeting early. The {@code orderId} field did not exist in the shop's first
 * version of this event: back then the store recorded that fifty points were
 * awarded and not what they were awarded for. Those old events are still in the
 * log, they still count towards every balance, and <em>they can never be
 * fixed</em>, because fixing them would mean rewriting history and the whole
 * value of the log is that nobody can.
 *
 * <p>So {@code orderId} is allowed to be absent, {@link #recordsItsOrder()} says
 * whether it is, and every piece of code that reads these events has to cope
 * with the gap — forever, in every version, for as long as the log exists. Use
 * {@link #beforeOrderIdsWereRecorded} to create one of the old shape.
 *
 * <p>That is what "you can version an event but never migrate it" means in
 * practice. It is not a warning about a future problem; it is a permanent
 * branch in the code, and it arrived the day somebody added a field.
 */
public record PointsAwarded(String customerId, int points, String orderId,
                            LocalDate on) implements LoyaltyEvent {

    /**
     * An event in the shape the shop wrote before it recorded order ids.
     *
     * <p>There is no constructor argument to leave out and no way to fill it in
     * afterwards. This factory exists so the gap is deliberate and named rather
     * than a null somebody forgot about.
     */
    public static PointsAwarded beforeOrderIdsWereRecorded(String customerId,
                                                           int points,
                                                           LocalDate on) {
        return new PointsAwarded(customerId, points, null, on);
    }

    /** Whether this event knows which order earned the points. */
    public boolean recordsItsOrder() {
        return orderId != null;
    }

    @Override
    public int effectOnBalance() {
        return points;
    }

    @Override
    public String because() {
        return recordsItsOrder()
                ? "earned " + points + " points on order " + orderId
                : "earned " + points + " points on an order this event never recorded";
    }
}
