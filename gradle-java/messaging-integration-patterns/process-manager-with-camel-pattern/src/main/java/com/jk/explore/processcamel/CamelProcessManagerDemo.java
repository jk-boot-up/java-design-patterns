package com.jk.explore.processcamel;

import java.util.ArrayList;
import java.util.List;
import org.apache.camel.CamelContext;
import org.apache.camel.CamelExecutionException;
import org.apache.camel.ProducerTemplate;
import org.apache.camel.impl.DefaultCamelContext;
import org.apache.camel.saga.InMemorySagaService;

/**
 * The five acts, with a Camel saga as the process manager.
 */
public final class CamelProcessManagerDemo {

    static final String GOOD = "4000000000000001";
    static final String DECLINED = "4000000000000002";

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();

        out.add("ONE. Each step hands on to the next.");
        Services chained = new Services();
        try (CamelContext camel = start(chained)) {
            ProducerTemplate send = camel.createProducerTemplate();
            send.sendBody("direct:chained", new Order("ORD-1", "KETTLE", GOOD));
            try {
                send.sendBody("direct:chained", new Order("ORD-3", "KETTLE", DECLINED));
            } catch (CamelExecutionException e) {
                out.add("  ORD-3, card declined: stopped at payments");
            }
        }
        out.add("  kettles in stock: " + chained.kettles() + " of 3, though only one was shipped");
        out.add("  nothing gave ORD-3's kettle back, and nothing knows where ORD-3 is");

        out.add("");
        out.add("TWO. A saga runs each order's journey.");
        Services services = new Services();
        try (CamelContext camel = start(services)) {
            ProducerTemplate send = camel.createProducerTemplate();
            send.sendBody("direct:order", new Order("ORD-1", "KETTLE", GOOD));
            services.awaitStatus("ORD-1", 5000);
            out.add("  ORD-1 replies: " + services.replies("ORD-1") + " -> " + services.status("ORD-1"));

            out.add("");
            out.add("THREE. The journey branches.");
            send.sendBody("direct:order", new Order("ORD-2", "TEAPOT", GOOD));
            services.awaitStatus("ORD-2", 5000);
            out.add("  ORD-2 replies: " + services.replies("ORD-2") + " -> " + services.status("ORD-2"));
            out.add("  main was out of stock, so the reserve step asked the partner warehouse");

            out.add("");
            out.add("FOUR. Payment is declined: Camel runs the undo steps.");
            try {
                send.sendBody("direct:order", new Order("ORD-3", "KETTLE", DECLINED));
            } catch (CamelExecutionException e) {
                // the sender still hears the failure
            }
            services.awaitStatus("ORD-3", 5000);
            services.awaitReply("ORD-3", "main RELEASED", 5000);
            out.add("  ORD-3 replies: " + services.replies("ORD-3"));
            out.add("  -> " + services.status("ORD-3") + "; kettles in stock: " + services.kettles() + " of 3");
            out.add("  email: " + services.emails());

            out.add("");
            out.add("FIVE. The bill.");
            out.add("  where is every order? " + services.statuses());
            out.add("  every step needs an undo step written for it, and undo is not the same as never happening");
            out.add("  the in-memory saga service forgets every journey on a restart; a durable coordinator is needed in production");
        }
        return out;
    }

    private static CamelContext start(Services services) throws Exception {
        CamelContext camel = new DefaultCamelContext();
        camel.addService(new InMemorySagaService());
        camel.addRoutes(new ShopRoutes(services));
        camel.start();
        return camel;
    }

    private CamelProcessManagerDemo() {
    }
}
