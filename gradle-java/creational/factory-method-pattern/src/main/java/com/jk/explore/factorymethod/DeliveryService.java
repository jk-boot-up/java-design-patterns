package com.jk.explore.factorymethod;

/**
 * The creator. It knows the whole shipping workflow but not a single
 * concrete courier class — subclasses decide that by overriding
 * {@link #createCourier()}.
 */
public abstract class DeliveryService {

    /** The factory method. Every subclass answers this one question. */
    protected abstract Courier createCourier();

    /** A human-readable name for the service tier. */
    public abstract String tier();

    /**
     * The workflow every tier shares. It is final on purpose: subclasses
     * change *which courier* is used, never the steps around it.
     */
    public final Shipment ship(Order order) {
        if (order.weightKg() <= 0) {
            throw new IllegalArgumentException("Order " + order.orderId() + " has no weight");
        }

        Courier courier = createCourier();

        System.out.println(tier() + ": preparing " + order.orderId()
                + " for " + order.destination() + " via " + courier.name());

        Shipment shipment = courier.dispatch(order);

        System.out.println(tier() + ": booked " + shipment.trackingId()
                + ", arriving in " + shipment.etaDays() + " day(s)");

        return shipment;
    }
}
