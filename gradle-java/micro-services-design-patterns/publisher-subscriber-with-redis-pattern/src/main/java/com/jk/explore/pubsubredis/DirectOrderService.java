package com.jk.explore.pubsubredis;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * The version with no publisher and no subscriber: the order service calls each service
 * that cares, by name, one after another.
 *
 * <p>It works, and it is the right shape for one caller and one callee. Its cost is the list
 * of names inside it. Every new service that wants to hear about an order is an edit to this
 * class.
 */
public class DirectOrderService {

    private final Map<String, List<String>> handled = new LinkedHashMap<>();

    public DirectOrderService() {
        handled.put("inventory", new ArrayList<>());
        handled.put("email", new ArrayList<>());
        handled.put("analytics", new ArrayList<>());
    }

    public void placeOrder(OrderEvent event) {
        callInventory(event);
        callEmail(event);
        callAnalytics(event);
    }

    private void callInventory(OrderEvent event) {
        handled.get("inventory").add(event.orderId());
    }

    private void callEmail(OrderEvent event) {
        handled.get("email").add(event.orderId());
    }

    private void callAnalytics(OrderEvent event) {
        handled.get("analytics").add(event.orderId());
    }

    public int servicesKnownByName() {
        return handled.size();
    }

    public List<String> handledBy(String service) {
        return List.copyOf(handled.get(service));
    }
}
