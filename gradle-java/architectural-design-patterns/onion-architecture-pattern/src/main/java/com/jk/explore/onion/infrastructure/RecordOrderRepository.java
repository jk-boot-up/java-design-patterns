package com.jk.explore.onion.infrastructure;

import com.jk.explore.onion.domain.model.Order;
import com.jk.explore.onion.domain.model.OrderLine;
import com.jk.explore.onion.domain.model.OrderRepository;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/** Stores each order as a line of text, as a file or a table might. Every save and find converts. */
public class RecordOrderRepository implements OrderRepository {

    private final Map<String, String> records = new HashMap<>();
    private int conversions;

    @Override
    public void save(Order order) {
        StringBuilder b = new StringBuilder(order.id());
        for (OrderLine l : order.lines()) {
            b.append('|').append(l.sku()).append(':').append(l.quantity()).append(':').append(l.unitCents());
        }
        b.append("|discount:").append(order.subtotalCents() - order.totalCents());
        records.put(order.id(), b.toString());
        conversions++;
    }

    @Override
    public Optional<Order> find(String id) {
        String record = records.get(id);
        if (record == null) {
            return Optional.empty();
        }
        String[] parts = record.split("\\|");
        List<OrderLine> lines = new ArrayList<>();
        long discount = 0;
        for (int i = 1; i < parts.length; i++) {
            String[] f = parts[i].split(":");
            if (f[0].equals("discount")) {
                discount = Long.parseLong(f[1]);
            } else {
                lines.add(new OrderLine(f[0], Integer.parseInt(f[1]), Long.parseLong(f[2])));
            }
        }
        Order order = new Order(parts[0], lines);
        order.applyDiscount(discount);
        conversions++;
        return Optional.of(order);
    }

    public String recordOf(String id) {
        return records.get(id);
    }

    public int conversions() {
        return conversions;
    }
}
