package com.jk.explore.transactionaloutbox;

/**
 * Save the order, then publish the event. Two lines, and everybody writes them.
 *
 * They look like one operation and they are not. Between the two lines the order exists and
 * nobody has been told about it, and if the process stops in that gap it stays that way
 * forever. Nothing retries, because nothing knows there is anything to retry: the order is
 * saved, so the next request finds a perfectly good order, and the message that should have
 * gone with it was never written down anywhere.
 *
 * <p>The failure has three properties that together make it one of the worst bugs in
 * distributed systems. It is <b>rare</b>, so it survives testing. It is <b>silent</b>, so
 * nothing alerts. And it is <b>invisible from the order</b>, so the investigation starts three
 * weeks later from the customer's side: "I was charged and never got a confirmation."
 *
 * <p>Reversing the two lines does not help. Publish first and a crash before the save has told
 * the world about an order that does not exist, and now Notifications has emailed a customer
 * about an order the Orders service has never heard of. Neither order of the two lines is
 * right, because the problem is not the order — it is that there are two of them.
 */
public final class NaiveOrderService {

    private final OrderDatabase database;
    private final MessageBroker broker;
    private final CallLog log;

    private boolean dieAfterSaving;

    public NaiveOrderService(OrderDatabase database, MessageBroker broker, CallLog log) {
        this.database = database;
        this.broker = broker;
        this.log = log;
    }

    /**
     * Scripts the crash that everybody's tests miss: the process stops after the save and
     * before the publish.
     */
    public void dieBetweenTheTwoLines() {
        this.dieAfterSaving = true;
    }

    /** Saves the order and tells the world. Usually. */
    public void placeOrder(Order order) {
        database.saveOnItsOwn(order);

        if (dieAfterSaving) {
            log.note("Orders", "DIED", "after the save, before the publish");
            throw new ProcessDiedException("between the save and the publish");
        }

        broker.publish(new OutboxMessage("msg-" + order.orderId(), "OrderPlaced",
                order.orderId(), order.total()));
    }
}
