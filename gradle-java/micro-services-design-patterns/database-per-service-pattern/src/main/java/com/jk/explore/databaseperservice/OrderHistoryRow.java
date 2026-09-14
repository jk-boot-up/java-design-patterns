package com.jk.explore.databaseperservice;

/** One row of the order history page, as the shopper sees it. */
public record OrderHistoryRow(String orderId, String sku, String productName, int quantity) {

    @Override
    public String toString() {
        return String.format("%s  %-32s x%d", orderId, productName, quantity);
    }
}
