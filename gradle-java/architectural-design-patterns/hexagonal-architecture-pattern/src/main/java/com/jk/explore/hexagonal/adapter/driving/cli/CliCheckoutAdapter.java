package com.jk.explore.hexagonal.adapter.driving.cli;

import com.jk.explore.hexagonal.core.PlaceOrderRequest;
import com.jk.explore.hexagonal.core.PlaceOrderRequest.RequestedLine;
import com.jk.explore.hexagonal.core.PlaceOrderResult;
import com.jk.explore.hexagonal.core.PlaceOrderService;

/**
 * <strong>The driving-side half of the forced change.</strong> The same
 * core, called from a shape as different from HTTP as reasonably possible: a
 * single command line, parsed by hand. {@link PlaceOrderService} is not
 * touched to make this adapter exist — it has no idea whether it is being
 * called from a web request, a command line, or a test.
 */
public class CliCheckoutAdapter {

    private final PlaceOrderService service;

    public CliCheckoutAdapter(PlaceOrderService service) {
        this.service = service;
    }

    /** {@code checkout cust-8801 ada@example.com ESP-001:1,GRD-014:1,BNS-220:2} */
    public String run(String commandLine) {
        String[] parts = commandLine.trim().split("\\s+");
        String customerId = parts[1];
        String email = parts[2];
        String[] rawLines = parts[3].split(",");

        RequestedLine[] lines = new RequestedLine[rawLines.length];
        for (int i = 0; i < rawLines.length; i++) {
            String[] skuAndQty = rawLines[i].split(":");
            lines[i] = new RequestedLine(skuAndQty[0], Integer.parseInt(skuAndQty[1]));
        }

        PlaceOrderResult result = service.place(PlaceOrderRequest.of(customerId, lines), email);

        if (result.placed()) {
            return "OK  " + result.orderId() + "  " + result.total();
        }
        return "ERR " + result.reason();
    }
}
