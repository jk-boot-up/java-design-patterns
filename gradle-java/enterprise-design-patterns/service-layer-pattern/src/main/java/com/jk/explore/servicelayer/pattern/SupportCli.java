package com.jk.explore.servicelayer.pattern;

import com.jk.explore.servicelayer.domain.OrderRejectedException;
import com.jk.explore.servicelayer.domain.OrderRequest;

/** The support command line: a second door onto the same {@code placeOrder}. */
public class SupportCli {

    private final OrderService service;

    public SupportCli(OrderService service) {
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
