package com.jk.explore.factorymethod;

public class GlobalCourier implements Courier {

    @Override
    public String name() {
        return "TransWorld Freight";
    }

    @Override
    public Shipment dispatch(Order order) {
        System.out.println("TransWorld Freight: filing customs papers for " + order.orderId());
        System.out.println("TransWorld Freight: handing over to the destination carrier in "
                + order.destination());
        return new Shipment(TrackingIds.withPrefix("TW"), name(), 9, 24.00 + order.weightKg() * 2.10);
    }
}
