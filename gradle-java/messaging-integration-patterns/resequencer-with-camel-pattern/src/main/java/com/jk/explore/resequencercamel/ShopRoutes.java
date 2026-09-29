package com.jk.explore.resequencercamel;

import org.apache.camel.builder.RouteBuilder;

/**
 * Four ways into the tracking page: straight through, Camel's stream resequencer, its batch
 * resequencer, and a stream resequencer with a short timeout for lost messages.
 */
public final class ShopRoutes extends RouteBuilder {

    private final OrderPage page;
    private final long gapTimeoutMillis;

    public ShopRoutes(OrderPage page, long gapTimeoutMillis) {
        this.page = page;
        this.gapTimeoutMillis = gapTimeoutMillis;
    }

    @Override
    public void configure() {
        // Before: applied in whatever order they arrive.
        from("direct:as-they-come").routeId("as-they-come")
                .bean(page, "apply");

        // Stream mode: releases each message as soon as everything before it has been seen,
        // and waits for a gap for at most gapTimeoutMillis before giving up on it.
        from("direct:stream").routeId("stream")
                .resequence(header("seq")).stream().timeout(gapTimeoutMillis)
                .bean(page, "apply");

        // Batch mode: collects a batch, sorts it, then releases the lot. Sorting by order, then
        // number, keeps each order's own sequence.
        from("direct:batch").routeId("batch")
                .resequence(simple("${header.order}-${header.seq}")).batch().size(5).timeout(10_000)
                .bean(page, "apply");
    }
}
