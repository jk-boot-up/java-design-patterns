package com.jk.explore.callback;

import java.util.ArrayList;
import java.util.List;

/** Remembers the order it is working on in a field, and reads the field when the answer comes. */
public class SharedFieldShop {

    private final Gateway gateway;
    private final List<String> log = new ArrayList<>();
    private String currentOrder;

    public SharedFieldShop(Gateway gateway) {
        this.gateway = gateway;
    }

    public void pay(String orderId) {
        currentOrder = orderId;
        gateway.charge(orderId, r -> log.add(currentOrder + " " + r.message()));
    }

    public List<String> log() {
        return log;
    }
}
