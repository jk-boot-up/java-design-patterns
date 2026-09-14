package com.jk.explore.transactionaloutbox;

/**
 * The same job done with an out-tray: save the order and the message in one commit, and tell
 * nobody.
 *
 * Read {@link #placeOrder} and notice what is missing. There is no call to the broker. This
 * service does not talk to the outside world at all — it writes two rows in one transaction
 * and returns. Publishing is somebody else's job, done later, by {@link OutboxRelay}.
 *
 * <p>That is what buys the guarantee. The only way for the order to exist is for the message
 * to exist beside it, because one commit created both. A crash before the commit leaves
 * nothing; a crash after it leaves an order and a message that will be published on the next
 * sweep. There is no gap to fall into, because there is only one write.
 *
 * <p>A second benefit comes free and is easy to miss: placing an order no longer depends on the
 * broker being up. The broker can be down for an hour and customers can still check out, with
 * the messages piling up in a table that costs nothing to write to.
 */
public final class OrderService {

    private final OrderDatabase database;
    private final CallLog log;

    private int nextMessage = 1;
    private boolean dieBeforeCommit;

    public OrderService(OrderDatabase database, CallLog log) {
        this.database = database;
        this.log = log;
    }

    /**
     * Scripts the process dying before the commit — the crash that costs nothing.
     *
     * The transaction is abandoned, so neither the order nor the message was ever written.
     * The customer sees checkout fail and tries again, which is the correct outcome and the
     * one everybody already knows how to handle.
     */
    public void dieBeforeCommitting() {
        this.dieBeforeCommit = true;
    }

    /** Saves the order and queues the announcement. One transaction, two rows. */
    public void placeOrder(Order order) {
        OrderDatabase.Transaction transaction = database.begin();
        transaction.save(order);
        transaction.save(new OutboxMessage("msg-" + nextMessage++, "OrderPlaced",
                order.orderId(), order.total()));

        if (dieBeforeCommit) {
            log.note("Orders", "DIED", "before the commit -- nothing was written");
            throw new ProcessDiedException("before the commit");
        }

        transaction.commit();
    }
}
