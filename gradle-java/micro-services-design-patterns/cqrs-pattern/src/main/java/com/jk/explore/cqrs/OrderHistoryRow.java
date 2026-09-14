package com.jk.explore.cqrs;

/**
 * One line of the order history page, stored exactly as it is shown.
 *
 * The product name is copied in here, which duplicates data that Catalog also holds, and
 * that duplication is the point rather than a mistake. Nothing has to be joined, looked
 * up or composed at read time; the page is already the page. The price of that is
 * {@code ProductRenamed} events and the code that applies them.
 */
public record OrderHistoryRow(String orderId, String sku, String productName,
                              int quantity, Money lineTotal, long placedAtMillis) {

    /** The same row with a new product name. Records are copied, not edited. */
    public OrderHistoryRow renamedTo(String newName) {
        return new OrderHistoryRow(orderId, sku, newName, quantity, lineTotal,
                placedAtMillis);
    }
}
