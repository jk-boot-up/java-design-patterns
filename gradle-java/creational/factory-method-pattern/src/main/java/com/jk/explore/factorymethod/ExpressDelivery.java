package com.jk.explore.factorymethod;

public class ExpressDelivery extends DeliveryService {

    @Override
    protected Courier createCourier() {
        return new AirCourier();
    }

    @Override
    public String tier() {
        return "Express";
    }
}
