package com.jk.explore.routingslipcamel;

import java.util.ArrayList;
import java.util.List;
import org.apache.camel.CamelContext;
import org.apache.camel.CamelExecutionException;
import org.apache.camel.ProducerTemplate;
import org.apache.camel.impl.DefaultCamelContext;

/**
 * The five acts, with Apache Camel's routingSlip() and, at the end, dynamicRouter().
 */
public final class CamelRoutingSlipDemo {

    static final List<Order> ORDERS = List.of(
            new Order("ORD-1", false, false, 40, false, 2500),
            new Order("ORD-2", true, false, 35, false, 3000),
            new Order("ORD-3", false, true, 30, false, 1800),
            new Order("ORD-4", false, false, 50, true, 64000));
    static final Order UNDERAGE = new Order("ORD-5", false, true, 16, false, 1200);

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        SlipWriter writer = new SlipWriter();

        out.add("ONE. One fixed pipeline for every order.");
        Steps fixed = new Steps();
        try (CamelContext camel = start(fixed, writer)) {
            ProducerTemplate send = camel.createProducerTemplate();
            ORDERS.forEach(o -> send.sendBody("direct:pipeline", o));
        }
        out.add("  " + ORDERS.size() + " orders x 6 steps = " + fixed.visits() + " visits; " + fixed.useful() + " did any work");

        out.add("");
        out.add("TWO. The slip, written once as each order sets off.");
        for (Order o : ORDERS) {
            out.add("  " + o.id() + " slip: " + writer.steps(o));
        }

        out.add("");
        out.add("THREE. routingSlip(header(\"slip\")): Camel follows each order's slip.");
        Steps slipped = new Steps();
        try (CamelContext camel = start(slipped, writer)) {
            ProducerTemplate send = camel.createProducerTemplate();
            ORDERS.forEach(o -> send.sendBody("direct:checkout", o));

            out.add("  " + slipped.visits() + " visits in all, " + slipped.useful() + " doing work");
            out.add("  ORD-2 went: " + slipped.went("ORD-2"));
            out.add("  no step knows which step comes after it");

            out.add("");
            out.add("FOUR. A new step: fraud check for orders over £500.");
            writer.addFraudCheck();
            send.sendBody("direct:checkout", ORDERS.get(3));
            out.add("  ORD-4 now went: " + slipped.went("ORD-4").subList(4, slipped.went("ORD-4").size()));
            out.add("  one rule added where slips are written; no route and no step changed");

            out.add("");
            out.add("FIVE. The bill: the slip is fixed when the order sets off.");
            try {
                send.sendBody("direct:checkout", UNDERAGE);
            } catch (CamelExecutionException e) {
                List<String> remaining = new ArrayList<>(writer.steps(UNDERAGE));
                remaining.removeAll(slipped.went("ORD-5"));
                out.add("  ORD-5 fails its age check: went " + slipped.went("ORD-5") + "; still on the slip: " + remaining);
            }
            out.add("  a slip can only stop; it cannot choose a new route from what happened on the way");
            send.sendBody("direct:checkout-dynamic", UNDERAGE);
            List<String> dyn = slipped.went("ORD-5");
            out.add("  Camel's dynamicRouter() decides each next step as it goes: ORD-5 went "
                    + dyn.subList(2, dyn.size()));
        }
        return out;
    }

    private static CamelContext start(Steps steps, SlipWriter writer) throws Exception {
        CamelContext camel = new DefaultCamelContext();
        camel.addRoutes(new ShopRoutes(steps, writer));
        camel.start();
        return camel;
    }

    private CamelRoutingSlipDemo() {
    }
}
