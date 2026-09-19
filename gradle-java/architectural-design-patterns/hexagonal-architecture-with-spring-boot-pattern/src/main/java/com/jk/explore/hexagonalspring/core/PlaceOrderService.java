package com.jk.explore.hexagonalspring.core;

import com.jk.explore.hexagonalspring.core.domain.Order;
import com.jk.explore.hexagonalspring.core.domain.OutOfStock;
import com.jk.explore.hexagonalspring.core.port.OrderStore;
import com.jk.explore.hexagonalspring.core.port.Payments;
import com.jk.explore.hexagonalspring.core.port.PlaceOrder;
import com.jk.explore.hexagonalspring.core.port.Warehouse;

import java.util.concurrent.atomic.AtomicInteger;

/**
 * The use case. Plain Java: no annotation, no Spring import, and it names its collaborators only
 * as ports. A configuration class elsewhere hands it the adapters.
 */
public class PlaceOrderService implements PlaceOrder {

    private final OrderStore orders;
    private final Warehouse warehouse;
    private final Payments payments;
    private final AtomicInteger sequence = new AtomicInteger();

    public PlaceOrderService(OrderStore orders, Warehouse warehouse, Payments payments) {
        this.orders = orders;
        this.warehouse = warehouse;
        this.payments = payments;
    }

    @Override
    public Receipt place(String customer, String sku, int quantity) {
        if (!warehouse.reserve(sku, quantity)) {
            throw new OutOfStock(sku);
        }
        long total = warehouse.priceOf(sku) * quantity;
        payments.charge(total);
        String id = String.format("ORD-%06d", sequence.incrementAndGet());
        orders.save(new Order(id, customer, sku, quantity, total));
        return new Receipt(id, total);
    }
}
