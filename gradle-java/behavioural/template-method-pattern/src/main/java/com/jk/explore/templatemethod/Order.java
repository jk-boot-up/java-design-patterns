package com.jk.explore.templatemethod;

import java.util.List;

/**
 * An order that is ready to be fulfilled.
 *
 * <p>The shipping address is allowed to be {@code null}, and that is the
 * whole reason this project has a hook. A download has nowhere to be sent,
 * so demanding an address of every order would make the digital route
 * impossible — but silently dropping the check for everybody would let a
 * warehouse order ship into the void.
 */
public record Order(String id, String customerEmail, String shippingAddress, List<OrderLine> lines) {

    public Order {
        if (id == null || id.isBlank()) {
            throw new IllegalArgumentException("an order needs an id");
        }
        lines = List.copyOf(lines);
    }

    /** An order going to a physical address. */
    public static Order shipped(String id, String email, String address, List<OrderLine> lines) {
        return new Order(id, email, address, lines);
    }

    /** An order with nowhere to ship to — a download, or a collection. */
    public static Order addressless(String id, String email, List<OrderLine> lines) {
        return new Order(id, email, null, lines);
    }

    public boolean hasShippingAddress() {
        return shippingAddress != null && !shippingAddress.isBlank();
    }

    /** Total number of physical units, which is what a packer counts. */
    public int itemCount() {
        return lines.stream().mapToInt(OrderLine::quantity).sum();
    }

    public Money subtotal() {
        return lines.stream().map(OrderLine::total).reduce(Money.zero(), Money::plus);
    }
}
