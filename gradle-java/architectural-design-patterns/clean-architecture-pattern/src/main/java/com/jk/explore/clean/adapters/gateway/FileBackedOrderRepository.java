package com.jk.explore.clean.adapters.gateway;

import com.jk.explore.clean.entities.Order;
import com.jk.explore.clean.entities.OrderLine;
import com.jk.explore.clean.usecases.OrderRepository;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * <strong>The other half of the forced change: an entirely new data
 * source.</strong> Simulates a flat, file-backed store — each save appends
 * one CSV-shaped line to an in-memory buffer standing in for a file on
 * disk, and a read parses the buffer back into entities. No real file I/O,
 * to keep the whole category offline, but a structurally different way of
 * keeping an order than a map ever was.
 *
 * <p>Implements the same {@link OrderRepository} the checkout path already
 * used, so it can be handed to a second {@code PlaceOrderInteractor}
 * instance — wired to the batch delivery mechanism in the demo — without
 * one line of {@code usecases} or {@code entities} changing.
 */
public class FileBackedOrderRepository implements OrderRepository {

    private final List<String> lines = new ArrayList<>();

    @Override
    public void save(Order order) {
        StringBuilder row = new StringBuilder();
        row.append(order.id()).append(';').append(order.customerId()).append(';')
                .append(order.total().pence());
        for (OrderLine line : order.lines()) {
            row.append(';').append(line.sku()).append(':').append(line.quantity());
        }
        lines.add(row.toString());
    }

    @Override
    public Optional<Order> find(String orderId) {
        return all().stream().filter(o -> o.id().equals(orderId)).findFirst();
    }

    @Override
    public List<Order> all() {
        // A read reconstructs entities from the flat rows -- the mapping cost
        // this project's written notes charge to every gateway.
        List<Order> orders = new ArrayList<>();
        for (String row : lines) {
            String[] fields = row.split(";");
            orders.add(Order.placed(fields[0], fields[1], List.of()));
        }
        return orders;
    }

    @Override
    public int count() {
        return lines.size();
    }

    @Override
    public String describe() {
        return "a flat file, one CSV-shaped line per order";
    }
}
