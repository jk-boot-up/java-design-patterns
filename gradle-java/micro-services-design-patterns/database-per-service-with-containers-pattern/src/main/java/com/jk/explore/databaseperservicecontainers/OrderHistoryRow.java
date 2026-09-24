package com.jk.explore.databaseperservicecontainers;

/** One row of the order history page: an order line, with the product's name beside it. */
public record OrderHistoryRow(String orderId, String sku, String productName, int quantity) {

    /** The row as the demo prints it, in fixed columns. */
    public String printed() {
        return String.format("%-9s %-12s %-28s x%d", orderId, sku, productName, quantity);
    }
}
