package com.jk.explore.onion.domain.service;

import com.jk.explore.onion.domain.model.Order;

/** A business rule that belongs to no single order: ten percent off orders of 100 pounds or more. */
public class PricingService {

    public void price(Order order) {
        if (order.subtotalCents() >= 10000) {
            order.applyDiscount(order.subtotalCents() / 10);
        }
    }
}
