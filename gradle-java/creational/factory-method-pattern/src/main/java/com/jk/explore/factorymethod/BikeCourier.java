package com.jk.explore.factorymethod;

public class BikeCourier implements Courier {

    @Override
    public String name() {
        return "CityRide Bikes";
    }

    @Override
    public Shipment dispatch(Order order) {
        System.out.println("CityRide Bikes: assigning a rider to " + order.orderId() + " right now");
        return new Shipment(TrackingIds.withPrefix("CR"), name(), 0, 8.00 + order.weightKg() * 0.30);
    }
}
