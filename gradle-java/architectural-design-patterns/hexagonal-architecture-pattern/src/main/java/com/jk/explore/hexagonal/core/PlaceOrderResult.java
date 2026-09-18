package com.jk.explore.hexagonal.core;

import com.jk.explore.hexagonal.core.domain.Money;

public record PlaceOrderResult(boolean placed, String orderId, Money total, String reason) {

    public static PlaceOrderResult placed(String orderId, Money total) {
        return new PlaceOrderResult(true, orderId, total, null);
    }

    public static PlaceOrderResult refused(String reason) {
        return new PlaceOrderResult(false, null, Money.ZERO, reason);
    }
}
