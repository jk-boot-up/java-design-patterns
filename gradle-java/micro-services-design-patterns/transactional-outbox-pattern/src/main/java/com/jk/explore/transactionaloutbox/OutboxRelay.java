package com.jk.explore.transactionaloutbox;

import java.util.List;

/**
 * The person who comes round to collect the out-tray.
 *
 * A separate job, running on its own, that reads the unsent messages, publishes each one, and
 * marks it sent. In a real shop it is a scheduled task polling a table every second, or a
 * process tailing the database's change log; here it is {@link #sweep()} and the demo calls it
 * when it wants a collection to happen.
 *
 * <p>Two things about the relay are worth saying out loud, because they are the pattern's
 * whole character.
 *
 * <p><b>It cannot lose a message.</b> The message is only marked sent after the broker has
 * accepted it. If the broker is down the publish fails, the message stays in the table, and
 * the next sweep tries again. Nobody had to write retry logic for this: the retry is a
 * consequence of where the message is stored.
 *
 * <p><b>It can send a message twice.</b> Between the broker accepting a message and
 * {@code markSent} recording that fact, there are two systems again — and this time nothing can
 * be done about it, because the second system is the broker. If the relay dies in that gap, the
 * message is still unsent as far as the table is concerned, and the next sweep publishes it
 * again. This is called <b>at-least-once delivery</b>, and it is not a bug in this class. It is
 * the price of never losing a message, and the only two options on offer are "possibly twice"
 * and "possibly never".
 *
 * <p>Which is why the receiver has to cope with duplicates, and why the next pattern in this
 * category is not optional.
 */
public final class OutboxRelay {

    private final OrderDatabase database;
    private final MessageBroker broker;
    private final CallLog log;

    private boolean dieAfterPublishing;

    public OutboxRelay(OrderDatabase database, MessageBroker broker, CallLog log) {
        this.database = database;
        this.broker = broker;
        this.log = log;
    }

    /**
     * Scripts the crash in the gap the pattern cannot close: the broker has taken the
     * message, and the relay dies before writing down that it has.
     */
    public void dieAfterPublishing() {
        this.dieAfterPublishing = true;
    }

    /**
     * One collection round. Publishes every unsent message and marks it sent.
     *
     * @return how many messages were published on this sweep
     */
    public int sweep() {
        List<OutboxMessage> waiting = database.unsent();
        if (waiting.isEmpty()) {
            log.note("Relay", "SWEEP", "out-tray empty");
            return 0;
        }

        int published = 0;
        for (OutboxMessage message : waiting) {
            try {
                broker.publish(message);
            } catch (ServiceUnavailableException brokerDown) {
                log.note("Relay", "LEFT-IN-TRAY", message.messageId()
                        + " -- broker down, it will go on the next sweep");
                continue;
            }

            if (dieAfterPublishing) {
                log.note("Relay", "DIED", "after publishing " + message.messageId()
                        + ", before marking it sent");
                throw new ProcessDiedException("between the publish and the mark-sent");
            }

            database.markSent(message.messageId());
            published++;
        }
        return published;
    }

    /** A sweep that survives the relay dying, so a demo can carry on to the next act. */
    public int sweepAndSurvive() {
        try {
            return sweep();
        } catch (ProcessDiedException died) {
            return 0;
        }
    }

    /** Turns the scripted crash off again, standing in for the relay being restarted. */
    public void restart() {
        this.dieAfterPublishing = false;
        log.note("Relay", "RESTARTED", "and the out-tray still has what it had");
    }
}
