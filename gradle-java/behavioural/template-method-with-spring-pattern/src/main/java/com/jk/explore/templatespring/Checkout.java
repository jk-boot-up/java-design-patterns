package com.jk.explore.templatespring;

import org.springframework.stereotype.Service;
import org.springframework.transaction.support.TransactionTemplate;

/**
 * Places an order and reserves its stock as one unit. {@link TransactionTemplate} owns the
 * fixed steps, begin, commit and roll back; the lambda is the part that differs.
 */
@Service
public class Checkout {

    private final OrderRepository orders;
    private final TransactionTemplate transaction;

    public Checkout(OrderRepository orders, TransactionTemplate transaction) {
        this.orders = orders;
        this.transaction = transaction;
    }

    public void placeAndReserve(String orderNumber, String customer, long totalPence, String sku, int quantity) {
        transaction.executeWithoutResult(status -> {
            orders.insert(orderNumber, customer, totalPence);
            orders.reserve(sku, quantity);
        });
    }
}
