package com.jk.explore.staticfactory;

public record Receipt(String orderId, Money subtotal, Money shipping,
                      String discountLabel, Money discountAmount, Money total) { }
