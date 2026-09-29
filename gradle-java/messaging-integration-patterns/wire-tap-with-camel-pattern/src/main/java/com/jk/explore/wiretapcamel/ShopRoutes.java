package com.jk.explore.wiretapcamel;

import org.apache.camel.builder.RouteBuilder;

/**
 * Checkout sends to direct:payments. The wire tap copies every message to direct:audit on its
 * own thread, and the payment service carries on regardless.
 */
public final class ShopRoutes extends RouteBuilder {

    private final PaymentService payment;
    private final Audit audit;
    private final boolean copyFirst;

    public ShopRoutes(PaymentService payment, Audit audit, boolean copyFirst) {
        this.payment = payment;
        this.audit = audit;
        this.copyFirst = copyFirst;
    }

    @Override
    public void configure() {
        if (copyFirst) {
            // onPrepare runs on the copy before it is sent: give the tap its own object.
            from("direct:payments").routeId("payments")
                    .wireTap("direct:audit")
                        .onPrepare(e -> e.getMessage().setBody(e.getMessage().getBody(PaymentMessage.class).copy()))
                    .bean(payment, "handle");
        } else {
            from("direct:payments").routeId("payments")
                    .wireTap("direct:audit")
                    .bean(payment, "handle");
        }
        from("direct:audit").routeId("audit").bean(audit, "record");
    }
}
