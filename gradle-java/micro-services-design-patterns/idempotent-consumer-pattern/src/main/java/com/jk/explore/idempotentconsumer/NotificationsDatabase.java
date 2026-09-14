package com.jk.explore.idempotentconsumer;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * The Notifications service's own database: the confirmations it has queued, and the ids of
 * the messages it has already handled.
 *
 * Two tables, and the second one is the pattern. It is the doorman's list of everyone he has
 * already stamped: nothing more than a set of ids with the time each was written.
 *
 * <p>{@link #begin()} gives a transaction that holds its writes until {@code commit}, so a
 * confirmation and the id of the message that caused it can land together or not at all. That
 * is the only reason this works. A dedupe list that can be written without the effect, or an
 * effect that can happen without the list being written, is not deduplication — it is a race
 * with a comment on it.
 */
public final class NotificationsDatabase {

    private final List<String> confirmations = new ArrayList<>();
    private final Map<String, Long> handled = new LinkedHashMap<>();
    private final SimulatedClock clock;
    private final CallLog log;

    public NotificationsDatabase(SimulatedClock clock, CallLog log) {
        this.clock = clock;
        this.log = log;
    }

    /** Writes held until they all land together, or never land at all. */
    public Transaction begin() {
        return new Transaction();
    }

    /** One transaction over both tables. */
    public final class Transaction {

        private final List<String> pendingConfirmations = new ArrayList<>();
        private final List<String> pendingIds = new ArrayList<>();

        private Transaction() {
        }

        /**
         * Queues a confirmation email by writing a row.
         *
         * Note that this writes a row rather than sending anything. That is deliberate, and it
         * is what makes the row and the message id commitable together — see the class comment
         * on {@link IdempotentNotificationConsumer} for why an effect that leaves the database
         * cannot be part of this transaction, and what to do about it.
         */
        public Transaction queueConfirmation(String text) {
            pendingConfirmations.add(text);
            return this;
        }

        /** Writes down that a message has been handled. */
        public Transaction recordHandled(String messageId) {
            pendingIds.add(messageId);
            return this;
        }

        public void commit() {
            confirmations.addAll(pendingConfirmations);
            for (String id : pendingIds) {
                handled.put(id, clock.millis());
            }
            log.note("NotifDb", "COMMIT", pendingConfirmations.size() + " confirmation(s) and "
                    + pendingIds.size() + " handled id(s) together");
        }
    }

    /** Queues a confirmation with no transaction and no id, the way the naive consumer does. */
    public void queueConfirmationOnItsOwn(String text) {
        confirmations.add(text);
        log.note("NotifDb", "COMMIT", "a confirmation on its own");
    }

    /** The doorman's check. */
    public boolean hasHandled(String messageId) {
        return handled.containsKey(messageId);
    }

    public List<String> confirmations() {
        return List.copyOf(confirmations);
    }

    public int confirmationsQueued() {
        return confirmations.size();
    }

    public int handledCount() {
        return handled.size();
    }

    /**
     * Throws away ids older than the given age — the housekeeping every dedupe store needs.
     *
     * The size of that window is a guess, and the honest cost of the pattern. Too short and a
     * duplicate that arrives after a long broker outage is treated as new. Too long and this
     * is a large table somebody has to operate.
     */
    public void forgetHandledOlderThan(long ageMillis) {
        long cutoff = clock.millis() - ageMillis;
        int before = handled.size();
        handled.entrySet().removeIf(entry -> entry.getValue() < cutoff);
        log.note("NotifDb", "EXPIRED", (before - handled.size()) + " id(s) forgotten, "
                + handled.size() + " kept");
    }
}
