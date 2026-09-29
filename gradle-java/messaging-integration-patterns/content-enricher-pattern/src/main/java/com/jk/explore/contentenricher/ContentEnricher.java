package com.jk.explore.contentenricher;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * The pattern: takes each thin order, adds the customer's details once, and passes the full message on.
 *
 * <p>An order whose customer cannot be found goes to a problem list with the
 * reason, instead of travelling on half-filled. With the cache switched on,
 * each customer is looked up only once.
 */
public final class ContentEnricher {

    private final CustomerDirectory directory;
    private final boolean cache;
    private final Map<String, Customer> cached = new HashMap<>();
    private final List<String> problems = new ArrayList<>();

    public ContentEnricher(CustomerDirectory directory, boolean cache) {
        this.directory = directory;
        this.cache = cache;
    }

    /** The enriched order, or empty if it went to the problem list. */
    public Optional<EnrichedOrder> enrich(OrderPlaced order) {
        Customer c = cache ? cached.get(order.customerId()) : null;
        if (c == null) {
            Optional<Customer> found = directory.find(order.customerId());
            if (found.isEmpty()) {
                problems.add(order.orderId() + ": no customer " + order.customerId());
                return Optional.empty();
            }
            c = found.get();
            if (cache) {
                cached.put(c.id(), c);
            }
        }
        return Optional.of(new EnrichedOrder(order.orderId(), order.customerId(), order.items(),
                c.name(), c.address(), c.tier()));
    }

    public List<String> problems() {
        return List.copyOf(problems);
    }
}
