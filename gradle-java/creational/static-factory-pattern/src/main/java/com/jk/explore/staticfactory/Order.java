package com.jk.explore.staticfactory;

public record Order(String orderId, String customerId, Money subtotal, Money shipping) { }
