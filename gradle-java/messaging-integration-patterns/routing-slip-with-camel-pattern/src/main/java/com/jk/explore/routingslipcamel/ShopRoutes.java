package com.jk.explore.routingslipcamel;

import org.apache.camel.Exchange;
import org.apache.camel.builder.RouteBuilder;

/**
 * Three ways through the steps: a fixed pipeline, a routing slip, and a dynamic router.
 */
public final class ShopRoutes extends RouteBuilder {

    private final Steps steps;
    private final SlipWriter writer;

    public ShopRoutes(Steps steps, SlipWriter writer) {
        this.steps = steps;
        this.writer = writer;
    }

    @Override
    public void configure() {
        // Before: every order visits every step.
        from("direct:pipeline").routeId("pipeline")
                .to("direct:validate", "direct:age-check", "direct:customs", "direct:charge", "direct:gift-wrap", "direct:pack");

        // The pattern: the slip is written once, then Camel follows it.
        from("direct:checkout").routeId("routing-slip")
                .setHeader("slip", method(writer, "slip"))
                .routingSlip(header("slip"));

        // Deciding the next step on the way, from what just happened.
        from("direct:checkout-dynamic").routeId("dynamic-router")
                .dynamicRouter(method(NextStep.class, "next"));

        for (String name : Steps.ALL) {
            from("direct:" + name).routeId(name)
                    .process(e -> steps.visit(name, e.getMessage().getBody(Order.class)));
        }
        from("direct:fraud-check").routeId("fraud-check")
                .process(e -> steps.visit("fraud-check", e.getMessage().getBody(Order.class)));
        // For the dynamic router: an age check that reports instead of throwing.
        from("direct:age-check-soft").routeId("age-check-soft")
                .process(e -> {
                    Order o = e.getMessage().getBody(Order.class);
                    try {
                        steps.visit("age-check", o);
                    } catch (IllegalStateException tooYoung) {
                        e.getMessage().setHeader("tooYoung", true);
                    }
                });
        from("direct:notify-customer").routeId("notify-customer")
                .process(e -> steps.visit("notify-customer", e.getMessage().getBody(Order.class)));
    }

    /** Used by dynamicRouter(): called before every step, it returns the next one, or null to finish. */
    public static final class NextStep {

        public static String next(Exchange exchange) {
            Order o = exchange.getMessage().getBody(Order.class);
            String last = exchange.getProperty(Exchange.SLIP_ENDPOINT, String.class);
            if (last == null) {
                return "direct:validate";
            }
            if (last.endsWith("validate")) {
                return o.ageRestricted() ? "direct:age-check-soft" : "direct:charge";
            }
            if (last.endsWith("age-check-soft")) {
                return exchange.getMessage().getHeader("tooYoung", false, Boolean.class)
                        ? "direct:notify-customer" : "direct:charge";
            }
            if (last.endsWith("charge")) {
                return "direct:pack";
            }
            return null;
        }
    }
}
