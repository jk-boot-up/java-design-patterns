package com.jk.explore.simplefactory;

public record PaymentRequest(String orderId, String customerId, double amount) {
}
