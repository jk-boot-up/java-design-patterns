package com.jk.explore.filtercamel;

import java.util.ArrayList;
import java.util.List;
import org.apache.camel.CamelContext;
import org.apache.camel.ProducerTemplate;
import org.apache.camel.impl.DefaultCamelContext;

/**
 * The five acts, with Apache Camel's filter() and Simple expressions.
 */
public final class CamelFilterDemo {

    static final List<OrderEvent> ORDERS = List.of(
            new OrderEvent("ORD-1", true, 6400, false),
            new OrderEvent("ORD-2", false, 1200, true),
            new OrderEvent("ORD-3", true, 2500, false),
            new OrderEvent("ORD-4", true, 8900, true),
            new OrderEvent("ORD-5", false, 7200, false),
            new OrderEvent("ORD-6", true, 5500, false),
            new OrderEvent("ORD-7", true, 900, false),
            new OrderEvent("ORD-8", false, 300, false),
            new OrderEvent("ORD-9", true, 4800, false),
            new OrderEvent("ORD-10", true, 1500, false));

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        Received giftWrap = new Received();
        Received loyalty = new Received();
        Received discarded = new Received();
        Rules rules = new Rules();

        out.add("ONE. Every service is handed every order.");
        try (CamelContext camel = context(new ShopRoutes(giftWrap, loyalty, discarded, rules, false))) {
            sendAll(camel);
        }
        out.add("  gift-wrap service handed " + giftWrap.orders().size() + " orders: it must open each and check for a gift");

        out.add("");
        out.add("TWO. filter(simple(\"${body.gift}\")) in front of the gift-wrap service.");
        giftWrap.clear();
        try (CamelContext camel = context(new ShopRoutes(giftWrap, loyalty, discarded, rules, true))) {
            ProducerTemplate send = camel.createProducerTemplate();
            for (OrderEvent o : ORDERS) {
                send.sendBody("direct:orders", o);
            }
            out.add("  gift-wrap service receives: " + giftWrap.orders() + "; the filter dropped "
                    + (ORDERS.size() - giftWrap.orders().size()));
            out.add("  checkout still sends every order to direct:orders; it does not know the filter exists");

            out.add("");
            out.add("THREE. Two conditions: registered, and over the threshold (£50).");
            out.add("  loyalty service receives: " + loyalty.orders());

            out.add("");
            out.add("FOUR. The threshold changes while the routes keep running.");
            loyalty.clear();
            discarded.clear();
            rules.setBonusThresholdPence(6000);
            for (OrderEvent o : ORDERS) {
                send.sendBody("direct:loyalty", o);
            }
            out.add("  threshold raised to £60: " + loyalty.orders());
            out.add("  no route was changed or restarted: the rule reads the value as each order passes");

            out.add("");
            out.add("FIVE. The bill, and a discard channel.");
            out.add("  orders the loyalty rule rejected, kept on direct:discard: " + discarded.orders().size()
                    + " " + discarded.orders());
            out.add("  a wrong rule would drop orders silently; with otherwise().to(discard) they can be counted");
            int jars = System.getProperty("java.class.path").split(java.io.File.pathSeparator).length;
            out.add("  the cost: Camel's Simple language to learn, and " + (jars > 10 ? "more than 10" : "about " + jars)
                    + " library files instead of none");
        }
        return out;
    }

    private static CamelContext context(ShopRoutes routes) throws Exception {
        CamelContext camel = new DefaultCamelContext();
        camel.addRoutes(routes);
        camel.start();
        return camel;
    }

    private static void sendAll(CamelContext camel) {
        ProducerTemplate send = camel.createProducerTemplate();
        for (OrderEvent o : ORDERS) {
            send.sendBody("direct:orders", o);
        }
    }

    private CamelFilterDemo() {
    }
}
