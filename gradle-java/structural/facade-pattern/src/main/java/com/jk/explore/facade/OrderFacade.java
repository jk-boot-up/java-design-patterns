package com.jk.explore.facade;

import java.util.UUID;

/**
 * Facade that hides the complexity of coordinating the Inventory, Payment,
 * Shipping and Notification subsystems behind a single, simple
 * {@link #placeOrder(OrderRequest)} method.
 */
public class OrderFacade {

    private final InventoryService inventoryService;
    private final PaymentService paymentService;
    private final ShippingService shippingService;
    private final NotificationService notificationService;

    public OrderFacade() {
        this.inventoryService = new InventoryService();
        this.paymentService = new PaymentService();
        this.shippingService = new ShippingService();
        this.notificationService = new NotificationService();
    }

    public OrderConfirmation placeOrder(OrderRequest request) {
        String orderId = "ORD-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();

        if (!inventoryService.reserveStock(request.productId(), request.quantity())) {
            throw new IllegalStateException("Product " + request.productId() + " is out of stock");
        }

        String paymentId = paymentService.charge(request.customerId(), request.amount());
        String trackingId = shippingService.scheduleShipment(orderId, request.shippingAddress());
        notificationService.sendOrderConfirmation(request.customerId(), orderId, trackingId);

        return new OrderConfirmation(orderId, paymentId, trackingId);
    }
}
