package com.jk.explore.factorymethod;

public class InternationalDelivery extends DeliveryService {

    @Override
    protected Courier createCourier() {
        return new GlobalCourier();
    }

    @Override
    public String tier() {
        return "International";
    }
}
