package com.jk.explore.producerconsumer.domain;

/** One order arriving at checkout. Packing is the slow step that follows it. */
public record Order(String id, String sku) {
}
