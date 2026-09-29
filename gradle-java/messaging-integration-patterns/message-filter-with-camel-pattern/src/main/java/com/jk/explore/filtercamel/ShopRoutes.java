package com.jk.explore.filtercamel;

import org.apache.camel.builder.RouteBuilder;

/**
 * The routes. direct:orders is what checkout sends to; every service listens through its own route.
 */
public final class ShopRoutes extends RouteBuilder {

    private final Received giftWrap;
    private final Received loyalty;
    private final Received discarded;
    private final Rules rules;
    private final boolean filtered;

    public ShopRoutes(Received giftWrap, Received loyalty, Received discarded, Rules rules, boolean filtered) {
        this.giftWrap = giftWrap;
        this.loyalty = loyalty;
        this.discarded = discarded;
        this.rules = rules;
        this.filtered = filtered;
    }

    @Override
    public void configure() {
        from("direct:orders").routeId("orders")
                .multicast().to("direct:gift-wrap", "direct:loyalty");

        if (!filtered) {
            // Before: every service is handed every order and must check for itself.
            from("direct:gift-wrap").routeId("gift-wrap").bean(giftWrap, "take");
            from("direct:loyalty").routeId("loyalty").stop();
            return;
        }

        // A message filter: only gift orders reach the gift-wrap service.
        from("direct:gift-wrap").routeId("gift-wrap")
                .filter(simple("${body.gift}"))
                    .bean(giftWrap, "take")
                .end();

        // Two filters in a row, the threshold read from Rules as each order passes. What either
        // filter rejects is sent to a discard channel instead of vanishing.
        from("direct:loyalty").routeId("loyalty")
                .setHeader("threshold", method(rules, "getBonusThresholdPence"))
                .choice()
                    .when(simple("${body.registered} && ${body.pence} > ${header.threshold}"))
                        .bean(loyalty, "take")
                    .otherwise()
                        .to("direct:discard")
                .end();

        from("direct:discard").routeId("discard").bean(discarded, "take");
    }
}
