package com.jk.explore.factorymethod;

public class AirCourier implements Courier {

    @Override
    public String name() {
        return "SkyLink Air";
    }

    @Override
    public Shipment dispatch(Order order) {
        System.out.println("SkyLink Air: booking " + order.orderId() + " onto tonight's flight");
        return new Shipment(TrackingIds.withPrefix("SL"), name(), 2, 12.50 + order.weightKg() * 1.20);
    }
}
