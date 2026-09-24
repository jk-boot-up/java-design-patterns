package com.jk.explore.databaseperservicecontainers;

/** One line of one order: who ordered, which product, how many. */
public record Order(String orderId, String customerId, String sku, int quantity) {
}
