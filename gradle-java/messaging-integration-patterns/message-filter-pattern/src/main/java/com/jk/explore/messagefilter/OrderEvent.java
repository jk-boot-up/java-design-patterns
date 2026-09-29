package com.jk.explore.messagefilter;

/**
 * "An order was placed": sent to every service that listens on the orders channel.
 */
public record OrderEvent(String orderId, String customer, boolean registered, long pence, boolean gift) {
}
