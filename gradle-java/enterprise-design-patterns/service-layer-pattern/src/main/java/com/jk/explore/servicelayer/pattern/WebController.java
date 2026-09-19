package com.jk.explore.servicelayer.pattern;

import com.jk.explore.servicelayer.domain.OrderRejectedException;
import com.jk.explore.servicelayer.domain.OrderRequest;

/** The web door. It translates a request into a call and a result into a reply, and holds no rule. */
public class WebController {

    private final OrderService service;

    public WebController(OrderService service) {
        this.service = service;
    }

    public String placeOrder(OrderRequest request) {
        try {
            service.placeOrder(request);
            return "placed";
        } catch (OrderRejectedException e) {
            return "refused: " + e.getMessage();
        }
    }
}
