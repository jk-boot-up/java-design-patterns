package com.jk.explore.eventbus;

/** The base of the order events, so a subscriber may ask for all of them. */
public interface OrderEvent {
    String orderId();
}
