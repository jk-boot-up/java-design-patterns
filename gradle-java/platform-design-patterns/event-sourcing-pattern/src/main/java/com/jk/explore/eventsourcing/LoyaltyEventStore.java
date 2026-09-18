package com.jk.explore.eventsourcing;

import java.util.ArrayList;
import java.util.List;

/**
 * The append-only log. Every fact the shop knows about loyalty points is in here,
 * in the order it happened, and nothing is ever updated or deleted.
 *
 * <p>There is no {@code update} method and no {@code delete} method, and that
 * absence is the entire design. A real implementation would be a database table
 * with an auto-incrementing id and no {@code UPDATE} grant, or a file opened in
 * append mode — the mechanism varies, the guarantee does not.
 *
 * <p>Two things here are instruments rather than parts of the pattern, and are
 * marked as such. {@link #eventsExamined()} counts how many events have been
 * read, because the cost of folding a long stream is a number this project
 * should print rather than describe. {@link #rewriteWithoutEventsFor} is the
 * escape hatch, and it exists so the demo can show what it breaks.
 */
public final class LoyaltyEventStore {

    private final List<LoyaltyEvent> events = new ArrayList<>();
    private int eventsExamined;

    /**
     * Adds one event to the end of the log. This is the only way in.
     *
     * <p>Note that nothing is validated here. The store does not know or care
     * whether a redemption leaves the balance negative — that is a decision for
     * the code that decides whether to append, made before the event exists. By
     * the time a fact is in the log it is history, and history does not get
     * vetoed.
     */
    public void append(LoyaltyEvent event) {
        events.add(event);
    }

    /** Every event for one customer, oldest first. */
    public List<LoyaltyEvent> eventsFor(String customerId) {
        return eventsFor(customerId, 0);
    }

    /**
     * Every event for one customer from a position in the log onwards.
     *
     * <p>The position is what makes snapshots possible: a snapshot says "the
     * balance was 140 as at event number 4,000", so rebuilding from it means
     * reading events 4,000 onwards instead of all of them.
     *
     * <p>Reading walks the whole log from that position and picks out the ones
     * that match, which is why {@link #eventsExamined()} climbs faster than the
     * number of events returned. A real store would have an index per customer;
     * the cost would be smaller and would still be there.
     */
    public List<LoyaltyEvent> eventsFor(String customerId, int fromPosition) {
        List<LoyaltyEvent> mine = new ArrayList<>();
        for (int i = fromPosition; i < events.size(); i++) {
            eventsExamined++;
            LoyaltyEvent event = events.get(i);
            if (event.customerId().equals(customerId)) {
                mine.add(event);
            }
        }
        return List.copyOf(mine);
    }

    /** How many events the log holds, which is also the next position. */
    public int size() {
        return events.size();
    }

    /** Instrument: how many events have been read since the meter was reset. */
    public int eventsExamined() {
        return eventsExamined;
    }

    /** Instrument: sets the read counter back to zero before a measurement. */
    public void resetMeter() {
        eventsExamined = 0;
    }

    /**
     * Removes every event belonging to one customer, and returns how many went.
     *
     * <p><strong>This is not an append-only operation and it is not part of the
     * pattern.</strong> It is here because a customer asking to be erased is a
     * legal obligation rather than a design preference, and "just delete the
     * events" is the first answer everybody reaches for. The demo calls this and
     * then shows the two things it breaks: the customer's own history is gone
     * beyond recovery, and any snapshot taken earlier still holds their balance,
     * so the data you deleted is still in the building.
     *
     * <p>The honest answers are harder and are named in the notes: keep the
     * events and encrypt the personal fields, then throw the key away, or keep
     * the shape of the event and blank the identity out of it.
     */
    public int rewriteWithoutEventsFor(String customerId) {
        int before = events.size();
        events.removeIf(event -> event.customerId().equals(customerId));
        return before - events.size();
    }
}
