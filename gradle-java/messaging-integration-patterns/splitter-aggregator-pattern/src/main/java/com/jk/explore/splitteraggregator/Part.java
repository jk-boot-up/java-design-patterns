package com.jk.explore.splitteraggregator;

/** One piece of an order: which order, which piece of how many, and its content. */
public record Part(String orderId, int index, int total, String content) {
}
