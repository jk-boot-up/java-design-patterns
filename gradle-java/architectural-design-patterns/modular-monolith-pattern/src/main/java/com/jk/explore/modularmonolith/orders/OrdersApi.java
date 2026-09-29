package com.jk.explore.modularmonolith.orders;

import com.jk.explore.modularmonolith.catalog.CatalogApi;
import com.jk.explore.modularmonolith.orders.internal.OrdersModule;
import com.jk.explore.modularmonolith.payments.PaymentsApi;

/**
 * The orders module's front door. It is given the other modules' front doors, never their insides.
 */
public interface OrdersApi {

    String placeOrder(String orderId, String sku, int qty, long pence);

    static OrdersApi create(CatalogApi catalog, PaymentsApi payments) {
        return new OrdersModule(catalog, payments);
    }
}
