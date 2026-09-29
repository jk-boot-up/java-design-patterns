package com.jk.explore.processcamel;

import org.apache.camel.builder.RouteBuilder;
import org.apache.camel.model.SagaPropagation;

/**
 * The process manager, written as a Camel saga: one route runs each order's journey; each step says
 * how to undo itself; Camel calls the undo steps when a later step fails, and the completion or
 * compensation route when the journey ends.
 */
public final class ShopRoutes extends RouteBuilder {

    private final Services services;

    public ShopRoutes(Services services) {
        this.services = services;
    }

    @Override
    public void configure() {
        // Before: each step simply hands on to the next; nobody owns the whole journey.
        from("direct:chained").routeId("chained")
                .bean(services, "reserveMainOnly")
                .bean(services, "pay")
                .bean(services, "ship");

        // The process manager: a saga. Completion and compensation say how the journey ends.
        from("direct:order").routeId("process-manager")
                .saga()
                    .completion("direct:done")
                    .compensation("direct:cancelled")
                    .option("orderId", simple("${body.id}"))
                .to("direct:reserve")
                .bean(services, "pay")
                .bean(services, "ship");

        // The reserve step joins the saga and names its own undo step.
        from("direct:reserve").routeId("reserve")
                .saga().propagation(SagaPropagation.MANDATORY)
                    .compensation("direct:release")
                    .option("orderId", simple("${body.id}"))
                    .option("sku", simple("${body.sku}"))
                .bean(services, "reserve");

        from("direct:release").routeId("release")
                .process(e -> services.release(e.getMessage().getHeader("orderId", String.class),
                        e.getMessage().getHeader("sku", String.class)));
        from("direct:done").routeId("done")
                .process(e -> services.done(e.getMessage().getHeader("orderId", String.class)));
        from("direct:cancelled").routeId("cancelled")
                .process(e -> services.cancelled(e.getMessage().getHeader("orderId", String.class)));
    }
}
