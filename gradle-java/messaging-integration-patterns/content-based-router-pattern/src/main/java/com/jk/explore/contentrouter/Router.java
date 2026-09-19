package com.jk.explore.contentrouter;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Looks inside each order and sends it to the channel whose rule it satisfies first. Senders and receivers
 * do not know about each other, or about the rules. If nothing matches, it goes to the fallback channel if
 * there is one, and is dropped, and counted, if not.
 */
public class Router {

    private final List<Route> routes = new ArrayList<>();
    private final Map<String, List<String>> channels = new LinkedHashMap<>();
    private final String fallback;
    private int dropped;

    public Router(String fallback) {
        this.fallback = fallback;
    }

    public Router route(String description, java.util.function.Predicate<Order> test, String channel) {
        routes.add(new Route(description, test, channel));
        return this;
    }

    /** Sends the order on, and says where it went. */
    public String send(Order order) {
        for (Route r : routes) {
            if (r.test().test(order)) {
                deliver(r.channel(), order);
                return r.channel();
            }
        }
        if (fallback != null) {
            deliver(fallback, order);
            return fallback;
        }
        dropped++;
        return null;
    }

    private void deliver(String channel, Order order) {
        channels.computeIfAbsent(channel, c -> new ArrayList<>()).add(order.id());
    }

    public Map<String, List<String>> channels() {
        return channels;
    }

    public int dropped() {
        return dropped;
    }

    public int rules() {
        return routes.size();
    }
}
