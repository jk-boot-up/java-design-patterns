package com.jk.explore.eventsourcing;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * A read-shaped copy of the customer's order history, kept up to date by the code
 * that handles writes.
 *
 * <p>This class is here to settle one confusion, and it does it by existing. It is
 * <strong>CQRS with no event sourcing anywhere in it.</strong> The write side keeps
 * a current-state row; this is a second model, shaped for the screen that displays
 * it, updated as writes go through. Reads come here, writes go there. That is the
 * whole of CQRS — Command Query Responsibility Segregation — and there is not an
 * event log in sight.
 *
 * <p>The other half of the confusion is settled by the rest of the project:
 * {@link EventSourcedLoyaltyAccounts} is <strong>event sourcing with no
 * CQRS</strong>. It stores events and it answers reads by folding the very same
 * events, with no separate read model at all.
 *
 * <p>So the two patterns are genuinely independent, and can be held apart with one
 * sentence each. <em>CQRS changes where reads come from. Event sourcing changes
 * what the writes store.</em> They are put together often because a log is an
 * awkward thing to read from directly and a projection fixes that — but "often
 * together" is not "the same thing", and treating them as one idea means arguing
 * about the wrong trade-off.
 */
public final class OrderHistoryReadModel {

    private final Map<String, List<String>> linesByCustomer = new LinkedHashMap<>();

    /** Called by the write side after an order goes through. */
    public void recordOrder(String customerId, String orderId, int pounds) {
        linesByCustomer.computeIfAbsent(customerId, id -> new ArrayList<>())
                .add("order " + orderId + " for £" + pounds);
    }

    /** What the customer's history page shows, ready to render. */
    public List<String> historyFor(String customerId) {
        return List.copyOf(linesByCustomer.getOrDefault(customerId, List.of()));
    }
}
