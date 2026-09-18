package com.jk.explore.layered.domain;

import java.util.List;

/**
 * A placed order.
 *
 * <p>The total is a field rather than a method, for the same reason the line
 * total is: it is the number the customer was charged, and it must not drift
 * when a price does.
 */
public record Order(String id,
                    String customerId,
                    List<OrderLine> lines,
                    Money total,
                    OrderStatus status) {

    public Order {
        lines = List.copyOf(lines);
    }

    public static Order placed(String id, String customerId, List<OrderLine> lines) {
        Money total = Money.ZERO;
        for (OrderLine line : lines) {
            total = total.plus(line.lineTotal());
        }
        return new Order(id, customerId, lines, total, OrderStatus.PLACED);
    }
}
