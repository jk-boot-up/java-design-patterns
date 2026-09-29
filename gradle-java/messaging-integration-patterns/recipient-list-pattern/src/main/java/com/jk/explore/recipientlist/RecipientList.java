package com.jk.explore.recipientlist;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.function.Function;

/**
 * The pattern: works out, for each message, the list of destinations that need it, and sends a copy to each.
 *
 * <p>The list comes from the message itself (which categories it contains,
 * how much it is worth) and from tables and rules that can change at run time.
 */
public final class RecipientList {

    private final Map<String, String> warehouseFor = new HashMap<>();
    private final List<Function<Order, Optional<String>>> rules = new ArrayList<>();

    public RecipientList stocks(String category, String warehouse) {
        warehouseFor.put(category, warehouse);
        return this;
    }

    public RecipientList rule(Function<Order, Optional<String>> rule) {
        rules.add(rule);
        return this;
    }

    public List<String> recipientsFor(Order order) {
        Set<String> to = new LinkedHashSet<>();
        for (String category : order.categories()) {
            to.add(warehouseFor.get(category));
        }
        for (Function<Order, Optional<String>> r : rules) {
            r.apply(order).ifPresent(to::add);
        }
        return new ArrayList<>(to);
    }

    /** Sends a copy to each recipient; returns the ones that could not be reached. */
    public List<String> send(Order order, Inboxes inboxes) {
        List<String> failed = new ArrayList<>();
        for (String r : recipientsFor(order)) {
            if (!inboxes.deliver(r, order)) {
                failed.add(r);
            }
        }
        return failed;
    }
}
