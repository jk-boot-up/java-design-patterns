package com.jk.explore.messagefilter;

import java.util.function.Consumer;
import java.util.function.Predicate;

/**
 * The pattern: stands between a channel and a receiver, and passes on only the messages that match its rule.
 *
 * <p>Neither the sender nor the receiver knows it is there. Filters can be
 * chained, and each counts what it dropped so drops are never invisible.
 */
public final class MessageFilter implements Consumer<OrderEvent> {

    private final String rule;
    private final Predicate<OrderEvent> keep;
    private final Consumer<OrderEvent> next;
    private int dropped;

    public MessageFilter(String rule, Predicate<OrderEvent> keep, Consumer<OrderEvent> next) {
        this.rule = rule;
        this.keep = keep;
        this.next = next;
    }

    @Override
    public void accept(OrderEvent event) {
        if (keep.test(event)) {
            next.accept(event);
        } else {
            dropped++;
        }
    }

    public int dropped() {
        return dropped;
    }

    public String rule() {
        return rule;
    }
}
