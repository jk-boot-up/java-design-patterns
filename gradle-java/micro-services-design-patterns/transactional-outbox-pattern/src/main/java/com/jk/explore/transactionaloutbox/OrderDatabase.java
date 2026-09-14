package com.jk.explore.transactionaloutbox;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * The Orders service's own database — orders in one table, the out-tray in another.
 *
 * The important thing this class provides is a real transaction. {@link #begin()} hands back
 * a {@link Transaction} that holds writes in its hand and does nothing to the tables until
 * {@code commit} is called. So a transaction that is abandoned half-way — because the process
 * died — leaves no trace at all, which is exactly what a database gives you and exactly what
 * a message broker cannot.
 *
 * <p>That is the one fact the whole pattern rests on: <b>the order row and the message row
 * are in the same database, so one commit covers both.</b> Either the order was placed and
 * the message is queued, or neither happened. There is no third outcome, and no amount of
 * care with two separate systems can give you that.
 */
public final class OrderDatabase {

    private final Map<String, Order> orders = new LinkedHashMap<>();
    private final Map<String, OutboxMessage> outbox = new LinkedHashMap<>();
    private final Set<String> sent = new LinkedHashSet<>();
    private final CallLog log;

    public OrderDatabase(CallLog log) {
        this.log = log;
    }

    /** Starts a transaction. Nothing it is given is visible until it commits. */
    public Transaction begin() {
        return new Transaction();
    }

    /**
     * Writes held until they all land together, or never land at all.
     *
     * Note what is not here: any way to commit half of it. That is not a simplification for
     * teaching — it is the property being borrowed.
     */
    public final class Transaction {

        private final List<Order> pendingOrders = new ArrayList<>();
        private final List<OutboxMessage> pendingMessages = new ArrayList<>();
        private boolean committed;

        private Transaction() {
        }

        public Transaction save(Order order) {
            pendingOrders.add(order);
            return this;
        }

        public Transaction save(OutboxMessage message) {
            pendingMessages.add(message);
            return this;
        }

        /** One commit, both tables. */
        public void commit() {
            if (committed) {
                throw new IllegalStateException("this transaction has already committed");
            }
            for (Order order : pendingOrders) {
                orders.put(order.orderId(), order);
            }
            for (OutboxMessage message : pendingMessages) {
                outbox.put(message.messageId(), message);
            }
            committed = true;
            log.note("OrderDb", "COMMIT", pendingOrders.size() + " order(s) and "
                    + pendingMessages.size() + " outbox message(s) together");
        }
    }

    /**
     * Saves an order with no transaction and no message, the way the naive service does it.
     *
     * There is nothing wrong with this method. What is wrong is what tends to follow it on
     * the next line.
     */
    public void saveOnItsOwn(Order order) {
        orders.put(order.orderId(), order);
        log.note("OrderDb", "COMMIT", "order " + order.orderId() + " on its own");
    }

    public Order find(String orderId) {
        return orders.get(orderId);
    }

    public int orderCount() {
        return orders.size();
    }

    /** The out-tray: messages written but not yet confirmed as published. */
    public List<OutboxMessage> unsent() {
        return outbox.values().stream()
                .filter(message -> !sent.contains(message.messageId()))
                .toList();
    }

    /**
     * Records that a message has gone out.
     *
     * The gap between the broker accepting a message and this line running is where the
     * pattern's price lives. See {@link OutboxRelay}.
     */
    public void markSent(String messageId) {
        sent.add(messageId);
        log.note("OrderDb", "MARKED-SENT", messageId);
    }

    public int outboxSize() {
        return outbox.size();
    }
}
