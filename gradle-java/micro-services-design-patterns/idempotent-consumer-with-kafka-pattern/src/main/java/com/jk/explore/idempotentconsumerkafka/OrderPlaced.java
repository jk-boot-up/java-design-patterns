package com.jk.explore.idempotentconsumerkafka;

import java.time.Instant;

/**
 * The message checkout sends when a customer places an order.
 *
 * <p>{@code messageId} is the part the pattern depends on. Checkout gives every message an
 * id of its own, and a message sent again carries the same id. Kafka's place number cannot
 * stand in for it: the same order sent twice by checkout lands at two different places.
 *
 * <p>{@code placedAt} is the time Kafka stamped on the message when it was written.
 */
public record OrderPlaced(String messageId, String orderId, long pence, Instant placedAt) {

    public static OrderPlaced of(int n) {
        String orderId = "ORD-" + n;
        return new OrderPlaced("placed-" + orderId, orderId, 7095 + 100L * (n - 1), Instant.EPOCH);
    }

    /** The message as it travels through Kafka: plain text, one line. */
    public String text() {
        return messageId + " " + orderId + " " + pence;
    }

    public static OrderPlaced read(String text, Instant placedAt) {
        String[] parts = text.split(" ");
        return new OrderPlaced(parts[0], parts[1], Long.parseLong(parts[2]), placedAt);
    }

    /** The body of the confirmation email this order should produce, once. */
    public String confirmation() {
        return "your order " + orderId + " for " + pence + " pence is confirmed";
    }
}
