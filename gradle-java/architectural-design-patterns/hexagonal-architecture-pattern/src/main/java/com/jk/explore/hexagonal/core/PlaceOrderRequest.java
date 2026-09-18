package com.jk.explore.hexagonal.core;

import java.util.List;

public record PlaceOrderRequest(String customerId, List<RequestedLine> lines) {

    public record RequestedLine(String sku, int quantity) {
    }

    public static PlaceOrderRequest of(String customerId, RequestedLine... lines) {
        return new PlaceOrderRequest(customerId, List.of(lines));
    }
}
