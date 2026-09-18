package com.jk.explore.eventsourcing;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * The pattern: the balance is not stored anywhere. It is worked out from the log
 * every time somebody asks.
 *
 * <p>Look for a field holding a number of points in this class. There isn't one.
 * {@link #balanceFor} starts at zero, walks the customer's events in order, adds
 * each event's effect, and returns what it reaches. That loop is event sourcing;
 * everything else in this file is a question the loop makes answerable.
 *
 * <p>Three of those questions are impossible for a stored balance, and they are
 * the reason to do this at all. {@link #explain} says why the number is what it
 * is, line by line. {@link #balanceOn} says what it was on any past day, without
 * anybody having thought to record that in advance. And {@link #duplicateAwards}
 * finds the customers a double-awarding bug touched, months later, because the
 * two awards are still sitting there with the same order id on them.
 *
 * <p>Snapshots are optional and off by default. Pass a {@link SnapshotStore} to
 * the two-argument constructor to turn them on, and read
 * {@link #balanceFor}'s comment for what that buys and what it then costs you.
 */
public final class EventSourcedLoyaltyAccounts implements LoyaltyAccounts {

    private final LoyaltyEventStore store;
    private final SnapshotStore snapshots;

    /** No snapshots: every balance is folded from the first event, every time. */
    public EventSourcedLoyaltyAccounts(LoyaltyEventStore store) {
        this(store, null);
    }

    /** With snapshots, which is the version a long-lived stream needs. */
    public EventSourcedLoyaltyAccounts(LoyaltyEventStore store, SnapshotStore snapshots) {
        this.store = store;
        this.snapshots = snapshots;
    }

    @Override
    public void award(String customerId, int points, String orderId, LocalDate on) {
        store.append(new PointsAwarded(customerId, points, orderId, on));
    }

    @Override
    public void redeem(String customerId, int points, String orderId, LocalDate on) {
        store.append(new PointsRedeemed(customerId, points, orderId, on));
    }

    @Override
    public void expire(String customerId, int points, LocalDate on) {
        store.append(new PointsExpired(customerId, points, on));
    }

    /**
     * The balance, folded from the log.
     *
     * <p>Without snapshots this reads the customer's whole history on every
     * call, which is fine for a hundred events and not fine for a hundred
     * thousand. With snapshots it starts from the last saved total and folds only
     * what happened since — cheaper, and now there are two places a balance can
     * come from, which is a second mechanism with its own way of being wrong.
     * {@link SnapshotStore} is where that trade is spelled out.
     */
    @Override
    public int balanceFor(String customerId) {
        Snapshot snapshot = snapshots == null ? null : snapshots.forCustomer(customerId);
        int running = snapshot == null ? 0 : snapshot.balance();
        int from = snapshot == null ? 0 : snapshot.upToPosition();
        for (LoyaltyEvent event : store.eventsFor(customerId, from)) {
            running += event.effectOnBalance();
        }
        return running;
    }

    /**
     * The balance as it stood at the end of a given day.
     *
     * <p>Nobody had to decide in advance that this question would be asked. It
     * is the same fold with a smaller set of events, and that is the property
     * that makes a log worth keeping: the questions do not have to be known when
     * the data is written.
     *
     * <p>Snapshots are deliberately ignored here. A snapshot is a shortcut to
     * <em>now</em>, and the past is before it.
     */
    public int balanceOn(String customerId, LocalDate day) {
        int running = 0;
        for (LoyaltyEvent event : store.eventsFor(customerId)) {
            if (!event.on().isAfter(day)) {
                running += event.effectOnBalance();
            }
        }
        return running;
    }

    /**
     * The answer support needs: one line per event, with the running total.
     *
     * <p>The running total is included on purpose. "You earned sixty, then spent
     * twenty-five" is a list of facts; the same list with the total beside it is
     * an explanation, and a customer on the phone can follow it.
     */
    public List<String> explain(String customerId) {
        List<String> lines = new ArrayList<>();
        int running = 0;
        for (LoyaltyEvent event : store.eventsFor(customerId)) {
            running += event.effectOnBalance();
            lines.add(String.format("%s  %-52s balance %d",
                    event.on(), event.because(), running));
        }
        return lines;
    }

    /**
     * Order ids that earned points more than once — the fingerprint of the bug.
     *
     * <p>This method is the project's strongest single argument, and it is worth
     * being clear about why. Nobody wrote it before the bug shipped. It was
     * written afterwards, to answer a question nobody had asked yet, and it works
     * on data that was already lying in the log — because an award that happened
     * twice is two events, and two events do not look like one no matter how much
     * later you look. On a current-state row the same investigation is not hard,
     * it is impossible: the second award was added to a number.
     */
    public List<String> duplicateAwards(String customerId) {
        Map<String, Integer> awardsPerOrder = new LinkedHashMap<>();
        for (LoyaltyEvent event : store.eventsFor(customerId)) {
            if (event instanceof PointsAwarded awarded && awarded.recordsItsOrder()) {
                awardsPerOrder.merge(awarded.orderId(), 1, Integer::sum);
            }
        }
        List<String> duplicated = new ArrayList<>();
        awardsPerOrder.forEach((orderId, count) -> {
            if (count > 1) {
                duplicated.add(orderId + " awarded " + count + " times");
            }
        });
        return List.copyOf(duplicated);
    }

    /**
     * The balance again, with a second award for the same order ignored.
     *
     * <p>This is the repair, and it is worth understanding what it does and does
     * not touch. <strong>No event was changed and none was deleted.</strong> The
     * duplicate awards are still in the log and always will be, because they did
     * happen — the shop really did hand out those points. What changed is the code
     * that reads the log, and every balance in the shop is now right because the
     * balance was never a stored number in the first place.
     *
     * <p>That is the moment event sourcing pays for everything it costs. On a
     * current-state row the same fix means working out the correct figure for each
     * affected customer from information you no longer have.
     *
     * <p>Two honest caveats. This rule is only correct because this shop awards
     * points once per order; a shop that legitimately awards twice for the same
     * order needs a different rule, and no amount of event sourcing will tell it
     * which awards were the mistake. And the alternative repair is often the better
     * one in practice: append a correcting event for each wrong award, so the log
     * says out loud that a mistake was made and put right, instead of a reader
     * having to know to call this method. What you must not do is edit the past.
     *
     * <p>Whichever repair you choose, every snapshot becomes untrustworthy the
     * moment the reading code changes, which is why {@link SnapshotStore#discardAll}
     * exists.
     */
    public int balanceWithDuplicateAwardsIgnored(String customerId) {
        int running = 0;
        List<String> ordersAlreadyCounted = new ArrayList<>();
        for (LoyaltyEvent event : store.eventsFor(customerId)) {
            if (event instanceof PointsAwarded awarded && awarded.recordsItsOrder()) {
                if (ordersAlreadyCounted.contains(awarded.orderId())) {
                    continue;
                }
                ordersAlreadyCounted.add(awarded.orderId());
            }
            running += event.effectOnBalance();
        }
        return running;
    }

    /** Captures the balance as at the log's current end, for {@link SnapshotStore}. */
    public Snapshot snapshotFor(String customerId, String computedBy) {
        return new Snapshot(customerId, balanceFor(customerId), store.size(), computedBy);
    }
}
