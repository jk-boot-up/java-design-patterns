package com.jk.explore.idempotentconsumerkafka;

import java.util.HashSet;
import java.util.Set;

/**
 * Keeps the ids it has handled in a set in this copy's memory, and skips any it has seen.
 * It is right about every duplicate that reaches the same copy. On Kafka, almost none do.
 */
public class RememberInMemory implements Handler {

    private final JustSend send;
    private final Set<String> handled = new HashSet<>();

    public RememberInMemory(Database database) {
        this.send = new JustSend(database);
    }

    @Override
    public boolean handle(OrderPlaced order) {
        if (handled.contains(order.messageId())) {
            return false;
        }
        send.handle(order);
        handled.add(order.messageId());
        return true;
    }

    public int remembered() {
        return handled.size();
    }
}
