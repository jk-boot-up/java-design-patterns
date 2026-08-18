package com.jk.explore.factorymethod;

public record Shipment(String trackingId, String carrier, int etaDays, double cost) {
}
