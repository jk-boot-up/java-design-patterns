package com.jk.explore.onion.ui;

import com.jk.explore.onion.application.PlaceOrderService;
import com.jk.explore.onion.domain.model.Order;
import com.jk.explore.onion.domain.model.OrderLine;
import java.util.List;

/** The outside: it turns a line of text into a use case, and the answer into text. */
public class ConsoleApi {

    private final PlaceOrderService service;

    public ConsoleApi(PlaceOrderService service) {
        this.service = service;
    }

    /** Input looks like: ORD-1 MUG 2 6000 */
    public String handle(String input) {
        String[] p = input.split(" ");
        Order order = service.place(p[0], List.of(new OrderLine(p[1], Integer.parseInt(p[2]), Long.parseLong(p[3]))));
        return order.id() + " total " + order.totalCents();
    }
}
