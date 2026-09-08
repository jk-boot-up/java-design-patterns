package com.jk.explore.observer;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * The subject: an order that announces its own status changes.
 *
 * <p>Search this class for the word "email". It is not here, and neither is
 * "inventory", "analytics" or "warehouse". The order knows it has listeners; it
 * does not know what any of them do, how many there are, or whether there are
 * any at all. Adding a fifth reaction to shipping is a new class plus one call
 * to {@link #addListener}, and this file does not change.
 *
 * <p>The list is a {@link CopyOnWriteArrayList} for one specific reason: a
 * listener is entirely within its rights to remove itself while it is being
 * notified -- a one-shot "email me when this ships" subscription is the obvious
 * case -- and an {@code ArrayList} would throw
 * {@code ConcurrentModificationException} at that. Copy-on-write iterates over
 * a snapshot, so a listener registered or removed during a notification simply
 * takes effect from the next one.
 */
public final class Order {

    private final String id;
    private final List<OrderListener> listeners = new CopyOnWriteArrayList<>();
    private OrderStatus status = OrderStatus.PLACED;

    public Order(String id) {
        this.id = Objects.requireNonNull(id, "id");
    }

    public String id() {
        return id;
    }

    public OrderStatus status() {
        return status;
    }

    /** How many listeners are attached. Used by the demo and the tests. */
    public int listenerCount() {
        return listeners.size();
    }

    public void addListener(OrderListener listener) {
        listeners.add(Objects.requireNonNull(listener, "listener"));
    }

    /** @return true if the listener was attached and has now been removed. */
    public boolean removeListener(OrderListener listener) {
        return listeners.remove(listener);
    }

    /**
     * Move the order to {@code next} and tell everyone.
     *
     * <p>Moving to the status the order is already in is not an event. Firing
     * one anyway would mean every listener has to defend itself against
     * duplicates, and the listener that forgets is the one that sends the
     * customer a second "your order has shipped" email.
     *
     * @return the listeners that threw, in the order they were notified. An
     *     empty list means every listener completed.
     */
    public List<ListenerFailure> moveTo(OrderStatus next) {
        Objects.requireNonNull(next, "next");
        if (next == status) {
            return List.of();
        }

        OrderEvent event = new OrderEvent(id, status, next);
        status = next;

        // The state is updated *before* the notification, so that a listener
        // which calls back into the order sees the world the event describes
        // rather than the one it replaced.
        List<ListenerFailure> failures = new ArrayList<>();
        for (OrderListener listener : listeners) {
            try {
                listener.onStatusChanged(event);
            } catch (RuntimeException e) {
                failures.add(ListenerFailure.of(listener, e));
            }
        }
        return List.copyOf(failures);
    }
}
