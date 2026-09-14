package com.jk.explore.transactionaloutbox;

/** One order, as the Orders service stores it. */
public record Order(String orderId, String customerId, Money total) {
}
