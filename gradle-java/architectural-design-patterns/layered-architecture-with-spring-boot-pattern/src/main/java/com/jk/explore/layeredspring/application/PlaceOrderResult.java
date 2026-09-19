package com.jk.explore.layeredspring.application;

/** What the outside world is told: an id, a total and a status, and nothing about costs. */
public record PlaceOrderResult(String orderId, long totalPence, String status) {
}
