package com.jk.explore.lenses;

/**
 * The customer who placed the order, and where to deliver.
 */
public record Customer(String name, Address address) {
}
