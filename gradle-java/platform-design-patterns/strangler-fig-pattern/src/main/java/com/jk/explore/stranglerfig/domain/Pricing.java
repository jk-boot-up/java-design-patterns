package com.jk.explore.stranglerfig.domain;

/** What an order costs: goods, VAT, delivery, and the total the customer pays. All in pence. */
public record Pricing(long subtotalPence, long vatPence, long deliveryPence, long totalPence) {
}
