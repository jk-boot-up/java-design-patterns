package com.jk.explore.mvc.infrastructure;

import com.jk.explore.mvc.domain.Order;

import java.util.List;
import java.util.Optional;

/**
 * Where orders are kept.
 *
 * <p><strong>Read the package name, because it is the whole of this project's
 * argument with the next one.</strong> This interface is an interface, and
 * swapping the implementation is therefore cheap — that is the forced change
 * this project performs. But it lives in {@code infrastructure}, the bottom
 * layer, and the layers above reach <em>down</em> to it. The domain imports the
 * storage package in order to say the word {@code OrderTable} at all.
 *
 * <p>Hexagonal architecture, which is the next project, changes exactly one
 * thing about this file: it moves it up into the core and lets storage
 * implement it. The interface is the same; the direction of the import
 * reverses. That single move is the step between the two architectures, and it
 * is worth knowing that it is only one move.
 */
public interface OrderTable {

    void save(Order order);

    Optional<Order> find(String orderId);

    List<Order> all();

    /** How many orders are held. Printed by the demo after the swap. */
    int count();

    /** A word for the demo to print, so the swap is visible in the output. */
    String describe();
}
