package com.jk.explore.idempotentconsumer;

import java.util.HashSet;
import java.util.Set;

/**
 * A {@code HashSet} of ids it has already seen, updated after the work is done. What everybody
 * writes, and it very nearly works.
 *
 * It even passes the obvious test: send the same message twice in a row and the second one is
 * ignored. Two things are wrong with it, and both of them only show up in production.
 *
 * <p><b>The memory is in the process.</b> The set lives in the heap, so a deploy, a restart or
 * a crash empties it. A duplicate that arrives after the restart is treated as brand new — and
 * a duplicate arriving after a restart is not an unlucky coincidence, because the restart is
 * often what caused the acknowledgement to be lost in the first place.
 *
 * <p><b>The id is written down after the work.</b> Between queueing the confirmation and adding
 * the id to the set there is a gap, and a crash in that gap loses the id while keeping the
 * effect. This is the doorman stamping the hand and being interrupted before writing the name
 * on the list.
 *
 * <p>Both faults have the same root: the id and the effect are stored in two different places,
 * so nothing can make them land together.
 */
public final class NaiveNotificationConsumer implements MessageConsumer {

    private final NotificationsDatabase database;
    private final CallLog log;

    private Set<String> seen = new HashSet<>();
    private boolean dieAfterQueueing;

    public NaiveNotificationConsumer(NotificationsDatabase database, CallLog log) {
        this.database = database;
        this.log = log;
    }

    @Override
    public String name() {
        return "Notifications";
    }

    /** Scripts the crash in the gap: the work is done, the id is not yet written. */
    public void dieAfterQueueing() {
        this.dieAfterQueueing = true;
    }

    /** A deploy. The database survives it; the {@code HashSet} does not. */
    public void restart() {
        this.seen = new HashSet<>();
        this.dieAfterQueueing = false;
        log.note(name(), "RESTARTED", "and its memory of what it has handled is empty");
    }

    @Override
    public void handle(Message message) {
        if (seen.contains(message.messageId())) {
            log.note(name(), "SKIPPED", message.messageId() + " -- already seen");
            return;
        }

        database.queueConfirmationOnItsOwn("your order " + message.orderId() + " for "
                + message.total() + " is confirmed");

        if (dieAfterQueueing) {
            log.note(name(), "DIED", "after queueing the email, before remembering the id");
            throw new ProcessDiedException("between the work and the record");
        }

        seen.add(message.messageId());
    }
}
