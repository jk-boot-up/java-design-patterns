package com.jk.explore.identitymap.domain;

/** An order, and the customer it belongs to. */
public record Order(int id, Customer customer) {
}
