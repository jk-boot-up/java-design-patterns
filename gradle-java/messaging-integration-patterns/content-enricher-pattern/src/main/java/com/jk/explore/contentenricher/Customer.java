package com.jk.explore.contentenricher;

/**
 * What the customer service knows about a customer: name, delivery address and loyalty tier.
 */
public record Customer(String id, String name, String address, String tier) {
}
