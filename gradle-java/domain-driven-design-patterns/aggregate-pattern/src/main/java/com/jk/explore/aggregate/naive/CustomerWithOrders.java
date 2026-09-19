package com.jk.explore.aggregate.naive;

import com.jk.explore.aggregate.domain.Money;
import com.jk.explore.aggregate.domain.Order;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * An aggregate drawn too big: the customer and every one of their orders, changed and saved as one thing.
 * Every order change is now a change to the customer, so two people working on different orders collide.
 */
public class CustomerWithOrders {

    private final Map<String, Order> orders = new LinkedHashMap<>();

    public void add(Order order) {
        orders.put(order.id().value(), order);
    }

    public void addLineTo(String orderId, String sku, Money price, int quantity) {
        orders.get(orderId).addLine(sku, price, quantity);
    }

    public int orderCount() {
        return orders.size();
    }

    public CustomerWithOrders copy() {
        CustomerWithOrders copy = new CustomerWithOrders();
        orders.forEach((id, order) -> copy.orders.put(id, order.copy()));
        return copy;
    }
}
