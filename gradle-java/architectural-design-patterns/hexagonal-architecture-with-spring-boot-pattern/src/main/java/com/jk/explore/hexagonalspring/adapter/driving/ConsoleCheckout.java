package com.jk.explore.hexagonalspring.adapter.driving;

import com.jk.explore.hexagonalspring.core.port.PlaceOrder;
import org.springframework.stereotype.Component;

/** A driving adapter: turns one typed line into a call on the port, and the answer into a line of text. */
@Component
public class ConsoleCheckout {

    private final PlaceOrder placeOrder;

    public ConsoleCheckout(PlaceOrder placeOrder) {
        this.placeOrder = placeOrder;
    }

    public String run(String line) {
        String[] parts = line.split(",");
        try {
            var receipt = placeOrder.place(parts[0].trim(), parts[1].trim(), Integer.parseInt(parts[2].trim()));
            return receipt.orderId() + " for " + String.format("£%d.%02d", receipt.totalPence() / 100, receipt.totalPence() % 100);
        } catch (RuntimeException e) {
            return "refused: " + e.getMessage();
        }
    }
}
