package com.jk.explore.sharding;

/**
 * An order, belonging to one customer.
 */
public record Order(String id, int customer, long pence) {
}
