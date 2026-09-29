package com.jk.explore.authorization;

/**
 * An order, and the customer who owns it.
 */
public record Order(String id, String owner, double total) {
}
