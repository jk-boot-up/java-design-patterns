package com.jk.explore.factorymethod;

public class PostalCourier implements Courier {

    @Override
    public String name() {
        return "Royal Post";
    }

    @Override
    public Shipment dispatch(Order order) {
        System.out.println("Royal Post: dropping " + order.orderId() + " into the postal network");
        return new Shipment(TrackingIds.withPrefix("RP"), name(), 5, 3.99 + order.weightKg() * 0.50);
    }
}
