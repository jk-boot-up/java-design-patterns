package com.jk.explore.idempotentconsumer;

/**
 * The pattern, and it is about fifteen lines: have I handled this id before? If yes, drop it.
 * If no, do the work and write the id down <em>in the same transaction</em>.
 *
 * The word <b>idempotent</b> means only this: handling the message twice has the same effect as
 * handling it once. It says nothing about how, and this class is the general way — remember the
 * ids. The doorman keeps a list of everyone he has stamped, and the name goes on the list in the
 * same motion as the stamp goes on the hand.
 *
 * <p><b>Why the transaction is the whole thing.</b> Take it away and you have the naive consumer
 * back, in one of its two shapes. Write the id first and a crash before the work means the
 * message is remembered as handled and the customer never gets their email — worse than a
 * duplicate, because nothing will ever retry. Write the id afterwards and a crash in between
 * loses the id and keeps the effect. Only committing them together removes the gap, and the
 * reason it can be committed together is that both writes are in this service's own database.
 *
 * <p><b>The uncomfortable part, said out loud.</b> That last sentence is a real constraint, not
 * a detail. The effect here is a row in a table, which is why it can share a transaction with
 * the id. If the effect were the actual email — a call to an outside provider — it could not,
 * and you would be back to two systems with a gap between them. The honest answer is the one
 * the previous pattern gives: write a row, and let an outbox relay do the sending. Which is why
 * these two patterns are taught together and are usually deployed together.
 */
public final class IdempotentNotificationConsumer implements MessageConsumer {

    private final NotificationsDatabase database;
    private final CallLog log;

    private boolean dieBeforeCommit;

    public IdempotentNotificationConsumer(NotificationsDatabase database, CallLog log) {
        this.database = database;
        this.log = log;
    }

    @Override
    public String name() {
        return "Notifications";
    }

    /**
     * Scripts the crash that costs nothing: the process dies before the commit, so neither the
     * confirmation nor the id was written, and the redelivery handles the message properly.
     */
    public void dieBeforeCommitting() {
        this.dieBeforeCommit = true;
    }

    /** A deploy. Nothing is lost, because nothing was being kept in memory. */
    public void restart() {
        this.dieBeforeCommit = false;
        log.note(name(), "RESTARTED", "and its list of handled ids is where it left it");
    }

    @Override
    public void handle(Message message) {
        if (database.hasHandled(message.messageId())) {
            log.note(name(), "IGNORED", message.messageId() + " -- handled already");
            return;
        }

        NotificationsDatabase.Transaction transaction = database.begin();
        transaction.queueConfirmation("your order " + message.orderId() + " for "
                + message.total() + " is confirmed");
        transaction.recordHandled(message.messageId());

        if (dieBeforeCommit) {
            log.note(name(), "DIED", "before the commit -- nothing was written");
            throw new ProcessDiedException("before the commit");
        }

        transaction.commit();
    }
}
