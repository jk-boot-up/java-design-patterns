package com.jk.explore.clean.adapters.controller;

import com.jk.explore.clean.usecases.PlaceOrderInput;
import com.jk.explore.clean.usecases.PlaceOrderInput.RequestedLine;
import com.jk.explore.clean.usecases.PlaceOrderInputBoundary;
import com.jk.explore.clean.usecases.PlaceOrderOutput;

import java.util.List;
import java.util.Map;

/**
 * An interface adapter: it depends on {@link PlaceOrderInputBoundary}, the
 * interface, never on {@code PlaceOrderInteractor}. This is the delivery
 * mechanism the demo starts with — a simulated HTTP request, a JSON body as
 * a {@code Map}. {@link BatchOrderController}, the forced change, is a
 * second one, added beside it.
 */
public class CheckoutController {

    private final PlaceOrderInputBoundary placeOrder;

    public CheckoutController(PlaceOrderInputBoundary placeOrder) {
        this.placeOrder = placeOrder;
    }

    @SuppressWarnings("unchecked")
    public String post(Map<String, Object> jsonBody) {
        String customerId = (String) jsonBody.get("customerId");
        String email = (String) jsonBody.get("email");
        List<Map<String, Object>> rawLines = (List<Map<String, Object>>) jsonBody.get("lines");

        RequestedLine[] lines = new RequestedLine[rawLines.size()];
        for (int i = 0; i < rawLines.size(); i++) {
            Map<String, Object> line = rawLines.get(i);
            lines[i] = new RequestedLine((String) line.get("sku"), (Integer) line.get("quantity"));
        }

        PlaceOrderOutput output = placeOrder.execute(PlaceOrderInput.of(customerId, email, lines));

        if (output.placed()) {
            return "{\"status\":201,\"orderId\":\"" + output.orderId()
                    + "\",\"total\":\"" + output.total() + "\"}";
        }
        return "{\"status\":422,\"reason\":\"" + output.reason() + "\"}";
    }
}
