package com.jk.explore.factorymethod;

public class SameDayDelivery extends DeliveryService {

    @Override
    protected Courier createCourier() {
        return new BikeCourier();
    }

    @Override
    public String tier() {
        return "Same Day";
    }
}
