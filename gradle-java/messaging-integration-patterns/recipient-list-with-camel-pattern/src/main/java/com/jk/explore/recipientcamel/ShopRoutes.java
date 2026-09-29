package com.jk.explore.recipientcamel;

import org.apache.camel.builder.RouteBuilder;

/**
 * direct:orders is the recipient list; each destination is a direct: endpoint with its own route.
 */
public final class ShopRoutes extends RouteBuilder {

    private final Warehouses warehouses;
    private final RoutingTable table;

    public ShopRoutes(Warehouses warehouses, RoutingTable table) {
        this.warehouses = warehouses;
        this.table = table;
    }

    @Override
    public void configure() {
        // Before: a copy of every order to every warehouse.
        from("direct:everyone").routeId("everyone")
                .multicast().to("direct:north", "direct:big-items", "direct:cold-store", "direct:south");

        // The pattern: each order goes only where the table says.
        from("direct:orders").routeId("recipient-list")
                .recipientList(method(table, "recipients"));

        for (String name : Warehouses.ALL) {
            from("direct:" + name).routeId(name)
                    .process(e -> warehouses.deliver(name, e.getMessage().getBody(Order.class)));
        }
    }
}
