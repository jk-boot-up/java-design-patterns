package com.jk.explore.hexagonal.core.port;

import com.jk.explore.hexagonal.core.domain.Order;

import java.util.List;
import java.util.Optional;

/**
 * Where orders are kept, named and shaped entirely in the core's own
 * vocabulary.
 *
 * <p><strong>Read where this interface lives, because it is this project's
 * whole argument with the one before it.</strong> In the layered-architecture
 * project, the equivalent interface lived in {@code infrastructure}, the
 * bottom layer, and the use case reached <em>down</em> to name it. Here it
 * lives in {@code core.port} — inside the core — and an adapter outside the
 * core reaches <em>up</em> to implement it. The interface is the same
 * three methods either way. Only the direction of the import reverses, and
 * that reversal is the entire difference between the two projects.
 */
public interface OrderStore {

    void save(Order order);

    Optional<Order> find(String orderId);

    List<Order> all();

    int count();

    /** A word for the demo to print, so a swap is visible in the output. */
    String describe();
}
