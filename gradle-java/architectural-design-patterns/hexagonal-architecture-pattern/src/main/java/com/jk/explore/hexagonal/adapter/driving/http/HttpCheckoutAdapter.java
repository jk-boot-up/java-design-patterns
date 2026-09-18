package com.jk.explore.hexagonal.adapter.driving.http;

import com.jk.explore.hexagonal.core.PlaceOrderRequest;
import com.jk.explore.hexagonal.core.PlaceOrderRequest.RequestedLine;
import com.jk.explore.hexagonal.core.PlaceOrderResult;
import com.jk.explore.hexagonal.core.PlaceOrderService;

import java.util.List;
import java.util.Map;

/**
 * A driving adapter: it calls <em>into</em> the core, rather than being
 * called by it. There is no real HTTP server here — a JSON-shaped request
 * body is simulated as a {@code Map}, and the response is a JSON-shaped
 * string — because the lesson is the shape of the call, not a socket.
 *
 * <p>The one thing to notice: this class depends on {@code core}, and
 * {@code core} has no idea this class, or HTTP, exists. That asymmetry is
 * the whole of "driving" versus "driven" — a driving adapter is a caller,
 * so it is always allowed to know about the core it calls.
 */
public class HttpCheckoutAdapter {

    private final PlaceOrderService service;

    public HttpCheckoutAdapter(PlaceOrderService service) {
        this.service = service;
    }

    /** Simulates {@code POST /orders} with a JSON body already parsed to a map. */
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

        PlaceOrderResult result = service.place(PlaceOrderRequest.of(customerId, lines), email);

        if (result.placed()) {
            return "{\"status\":201,\"orderId\":\"" + result.orderId()
                    + "\",\"total\":\"" + result.total() + "\"}";
        }
        return "{\"status\":422,\"reason\":\"" + result.reason() + "\"}";
    }
}
