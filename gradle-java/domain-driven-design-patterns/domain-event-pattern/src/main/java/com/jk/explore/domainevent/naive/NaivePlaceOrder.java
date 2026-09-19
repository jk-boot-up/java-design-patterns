package com.jk.explore.domainevent.naive;

import com.jk.explore.domainevent.infrastructure.Journal;

import java.util.HashSet;
import java.util.Set;

/**
 * Placing an order the way it is first written: the order code calls stock, email and analytics itself,
 * one after another. It knows all three, and the day one of them fails it is in a half-done state.
 */
public class NaivePlaceOrder {

    private final Journal journal;
    private final Set<String> savedOrders = new HashSet<>();
    private boolean mailServerDown;

    public NaivePlaceOrder(Journal journal) {
        this.journal = journal;
    }

    public void mailServerDown(boolean down) {
        this.mailServerDown = down;
    }

    public boolean isSaved(String orderId) {
        return savedOrders.contains(orderId);
    }

    public void place(String orderId, String customer, long totalPence) {
        savedOrders.add(orderId);
        journal.add("stock: reserved for " + orderId);
        if (mailServerDown) {
            throw new IllegalStateException("mail server timed out");
        }
        journal.add("email: confirmed " + orderId + " to " + customer);
        journal.add("analytics: counted " + orderId + " for " + totalPence + " pence");
    }
}
