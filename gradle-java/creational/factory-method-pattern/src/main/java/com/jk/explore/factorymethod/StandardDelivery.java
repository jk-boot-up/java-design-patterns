package com.jk.explore.factorymethod;

public class StandardDelivery extends DeliveryService {

    @Override
    protected Courier createCourier() {
        return new PostalCourier();
    }

    @Override
    public String tier() {
        return "Standard";
    }
}
