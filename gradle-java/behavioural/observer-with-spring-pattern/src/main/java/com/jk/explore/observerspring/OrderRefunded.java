package com.jk.explore.observerspring;

/** A second kind of event, which nobody listens to. */
public record OrderRefunded(String orderId) {
}
