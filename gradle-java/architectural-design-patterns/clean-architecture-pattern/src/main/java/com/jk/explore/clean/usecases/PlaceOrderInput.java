package com.jk.explore.clean.usecases;

import java.util.List;

/**
 * A DTO, crossing the boundary from whichever adapter called in. It carries
 * plain data — no entity, no domain type richer than a string and a number
 * — because a DTO is what a boundary is allowed to pass, and an entity is
 * not.
 */
public record PlaceOrderInput(String customerId, List<RequestedLine> lines, String contact) {

    public record RequestedLine(String sku, int quantity) {
    }

    public static PlaceOrderInput of(String customerId, String contact, RequestedLine... lines) {
        return new PlaceOrderInput(customerId, List.of(lines), contact);
    }
}
