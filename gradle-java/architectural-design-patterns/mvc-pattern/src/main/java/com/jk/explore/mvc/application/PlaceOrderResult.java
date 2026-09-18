package com.jk.explore.mvc.application;

import com.jk.explore.mvc.domain.Money;

/**
 * What came back: either an order was placed, or it was refused and there is a
 * reason to show the customer.
 *
 * <p>A refusal is a returned value rather than an escaping exception, because
 * "we only have two grinders" is an ordinary outcome of checking out and the
 * presentation layer has to render it. Exceptions are for the layer below to
 * raise and this layer to absorb — which is exactly what happens to a declined
 * card.
 */
public record PlaceOrderResult(boolean placed, String orderId, Money total, String reason) {

    public static PlaceOrderResult placed(String orderId, Money total) {
        return new PlaceOrderResult(true, orderId, total, null);
    }

    public static PlaceOrderResult refused(String reason) {
        return new PlaceOrderResult(false, null, Money.ZERO, reason);
    }
}
