package com.jk.explore.servicelayer.domain;

import java.util.List;

/**
 * An order, and the business rules about it: a cart must not be empty, a
 * quantity must be positive, and free delivery starts at a set total. The
 * rules are here, in the domain. Who calls them, and in what order, is the
 * service layer's job.
 */
public class Order {

    public static final int FREE_DELIVERY_FROM_PENCE = 5_000;

    private final int id;
    private final int customerId;
    private final List<CartLine> lines;
    private final int totalPence;

    private Order(int id, int customerId, List<CartLine> lines, int totalPence) {
        this.id = id;
        this.customerId = customerId;
        this.lines = lines;
        this.totalPence = totalPence;
    }

    public static Order from(int id, OrderRequest request, List<Product> products) {
        if (request.lines().isEmpty()) {
            throw new OrderRejectedException("the cart is empty");
        }
        int total = 0;
        for (CartLine line : request.lines()) {
            if (line.quantity() <= 0) {
                throw new OrderRejectedException("quantity must be positive");
            }
            total += products.get(line.productId() - 1).pricePence() * line.quantity();
        }
        return new Order(id, request.customerId(), request.lines(), total);
    }

    public int id() {
        return id;
    }

    public int customerId() {
        return customerId;
    }

    public List<CartLine> lines() {
        return lines;
    }

    public int totalPence() {
        return totalPence;
    }

    public boolean deliveryIsFree() {
        return totalPence >= FREE_DELIVERY_FROM_PENCE;
    }
}
