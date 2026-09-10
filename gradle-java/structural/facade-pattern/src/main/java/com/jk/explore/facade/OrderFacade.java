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
        this(new InventoryService(), new PaymentService(), new ShippingService(), new NotificationService());
    }

    /**
     * Package-private, and deliberately so: callers get the no-argument
     * constructor above, while the tests can hand in subsystems that record
     * what they were asked or refuse the stock. It is not a second public API.
     */
    OrderFacade(InventoryService inventoryService, PaymentService paymentService,
                ShippingService shippingService, NotificationService notificationService) {
        this.inventoryService = inventoryService;
        this.paymentService = paymentService;
        this.shippingService = shippingService;
        this.notificationService = notificationService;
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
