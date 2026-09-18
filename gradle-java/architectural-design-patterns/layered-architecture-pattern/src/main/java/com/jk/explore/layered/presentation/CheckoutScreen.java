package com.jk.explore.layered.presentation;

import com.jk.explore.layered.application.PlaceOrderRequest;
import com.jk.explore.layered.application.PlaceOrderResult;
import com.jk.explore.layered.application.PlaceOrderService;

/**
 * The top layer: turn what a customer typed into a call on the application
 * layer, and turn what came back into words.
 *
 * <p>There is no web server here and no routing, because routing is not the
 * pattern. Underneath every framework, a controller is this: a method that
 * takes a request, calls one thing, and formats the answer. Strip the
 * annotations off any controller you have ever written and this is what is
 * left.
 *
 * <p><strong>What this class must never learn.</strong> It has two imports and
 * both are the application layer. It does not know whether orders are kept in a
 * map, a log, or a filing cabinet, and the architecture test in this project
 * exists to keep it that way. The single call that would ruin the whole
 * arrangement — reaching past the application layer and touching storage
 * directly — is one line of perfectly ordinary Java, it compiles, and nothing
 * in the build objects to it unless something is asked to.
 */
public class CheckoutScreen {

    private final PlaceOrderService placeOrder;

    public CheckoutScreen(PlaceOrderService placeOrder) {
        this.placeOrder = placeOrder;
    }

    public String checkout(PlaceOrderRequest request, String customerEmail) {
        PlaceOrderResult result = placeOrder.place(request, customerEmail);
        if (result.placed()) {
            return "Order " + result.orderId() + " placed. Total " + result.total() + ".";
        }
        return "Sorry — " + result.reason() + ".";
    }
}
