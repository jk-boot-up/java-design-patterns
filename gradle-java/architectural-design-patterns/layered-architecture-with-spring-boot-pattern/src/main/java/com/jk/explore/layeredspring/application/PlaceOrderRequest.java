package com.jk.explore.layeredspring.application;

public record PlaceOrderRequest(String customer, String sku, int quantity) {
}
