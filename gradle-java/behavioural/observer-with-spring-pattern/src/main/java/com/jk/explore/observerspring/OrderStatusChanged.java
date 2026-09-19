package com.jk.explore.observerspring;

/** The message: which order moved from which status to which. It carries no reference back to the order. */
public record OrderStatusChanged(String orderId, String from, String to) {
}
