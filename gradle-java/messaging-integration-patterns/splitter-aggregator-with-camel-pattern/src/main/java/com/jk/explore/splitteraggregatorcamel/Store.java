package com.jk.explore.splitteraggregatorcamel;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.apache.camel.CamelContext;
import org.apache.camel.ProducerTemplate;
import org.apache.camel.impl.DefaultCamelContext;

/**
 * The online store, running on Apache Camel. It owns the running Camel engine, the routes, and the one
 * object that sends messages into them. Everything the demo and the tests do goes through here, so the
 * engine is started once and stopped once.
 */
public class Store implements AutoCloseable {

    /** The three warehouses, in the order the customer's lines are in. */
    public static final List<String> WAREHOUSES = List.of("Leeds", "Reading", "Glasgow");

    private final CamelContext camel = new DefaultCamelContext();
    private final ProducerTemplate send;

    public final OnePicker onePicker = new OnePicker();
    public final Warehouse warehouse = new Warehouse();
    public final List<Shipment> collected = new ArrayList<>();
    public final Results results = new Results();
    public final StoreRoutes routes;

    public Store() {
        routes = new StoreRoutes(onePicker, warehouse, collected, results);
        try {
            camel.addRoutes(routes);
        } catch (Exception e) {
            throw new IllegalStateException("Camel could not build the store's routes.", e);
        }
        camel.start();
        send = camel.createProducerTemplate();
    }

    /** The same three-line basket every time, under whatever order number the act needs. */
    public static Order order(String id) {
        return new Order(id, List.of(
                new OrderLine("MUG-BLUE", 2, 799, "Leeds"),
                new OrderLine("ESP-001", 1, 24999, "Reading"),
                new OrderLine("TEA-050", 5, 349, "Glasgow")));
    }

    /** Sends a whole order in at the splitter. A named closed warehouse simply never answers. */
    public void checkout(Order order, String gatherTo, String closedWarehouse) {
        Map<String, Object> headers = new HashMap<>();
        headers.put("gatherTo", gatherTo);
        headers.put("closedWarehouse", closedWarehouse);
        send.sendBodyAndHeaders("direct:checkout", order, headers);
    }

    /** Hands one already-picked shipment straight to an aggregator, which is how arrival order is chosen. */
    public void deliver(Shipment shipment, String gatherTo) {
        Map<String, Object> headers = new HashMap<>();
        headers.put("orderId", shipment.orderId());
        headers.put("shipmentCount", shipment.of());
        send.sendBodyAndHeaders(gatherTo, shipment, headers);
    }

    /** The before picture: the whole order handed to one worker, who returns what it comes to in pence. */
    public int onePickerTotal(Order order) {
        return send.requestBody("direct:one-picker", order, Integer.class);
    }

    @Override
    public void close() {
        camel.stop();
    }
}
