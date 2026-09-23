package com.jk.explore.splitteraggregatorcamel;

import java.util.List;

/** One customer's basket: an order number, and the lines in it. */
public record Order(String id, List<OrderLine> lines) {

    public int totalPence() {
        return lines.stream().mapToInt(OrderLine::linePence).sum();
    }
}
