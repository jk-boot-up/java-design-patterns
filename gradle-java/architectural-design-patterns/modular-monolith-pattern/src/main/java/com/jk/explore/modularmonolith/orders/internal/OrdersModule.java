package com.jk.explore.modularmonolith.orders.internal;

import com.jk.explore.modularmonolith.catalog.CatalogApi;
import com.jk.explore.modularmonolith.orders.OrdersApi;
import com.jk.explore.modularmonolith.payments.PaymentsApi;

/**
 * Inside orders: reserves stock through the catalogue's front door, then charges through payments'.
 */
public final class OrdersModule implements OrdersApi {

    private final CatalogApi catalog;
    private final PaymentsApi payments;

    public OrdersModule(CatalogApi catalog, PaymentsApi payments) {
        this.catalog = catalog;
        this.payments = payments;
    }

    @Override
    public String placeOrder(String orderId, String sku, int qty, long pence) {
        if (!catalog.reserve(sku, qty)) {
            return orderId + " refused: only " + catalog.stock(sku) + " " + sku + " left";
        }
        return orderId + " placed, " + payments.charge(orderId, pence);
    }
}
