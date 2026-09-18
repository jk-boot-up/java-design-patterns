package com.jk.explore.mvc.application;

import java.util.List;

/**
 * What the outside world asks for, in the application layer's own words.
 *
 * <p>Note what is <em>not</em> here: no prices, no product names, no totals.
 * A caller says who they are and what they want, and everything else is worked
 * out inside. A request object that carried a total would be a request object
 * that let the caller decide what to charge.
 */
public record PlaceOrderRequest(String customerId, List<RequestedLine> lines) {

    public record RequestedLine(String sku, int quantity) {
    }

    public static PlaceOrderRequest of(String customerId, RequestedLine... lines) {
        return new PlaceOrderRequest(customerId, List.of(lines));
    }
}
