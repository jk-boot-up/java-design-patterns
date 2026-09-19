package com.jk.explore.chainspring;

public record CheckoutRequest(String customer, boolean addressValid, boolean inStock, int fraudScore, long amountPence) {
}
