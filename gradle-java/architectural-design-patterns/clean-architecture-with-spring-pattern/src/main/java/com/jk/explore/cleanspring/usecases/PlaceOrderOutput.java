package com.jk.explore.cleanspring.usecases;

import com.jk.explore.cleanspring.entities.Money;

/** The DTO crossing back out. Also plain data, for the same reason. */
public record PlaceOrderOutput(boolean placed, String orderId, Money total, String reason) {

    public static PlaceOrderOutput placed(String orderId, Money total) {
        return new PlaceOrderOutput(true, orderId, total, null);
    }

    public static PlaceOrderOutput refused(String reason) {
        return new PlaceOrderOutput(false, null, Money.ZERO, reason);
    }
}
