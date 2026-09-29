package com.jk.explore.translatorcamel;

import java.util.ArrayList;
import java.util.List;
import org.apache.camel.CamelContext;
import org.apache.camel.CamelExecutionException;
import org.apache.camel.ProducerTemplate;
import org.apache.camel.impl.DefaultCamelContext;

/**
 * The five acts, with Apache Camel doing the translating and the routing.
 */
public final class CamelTranslatorDemo {

    static final String WEB = "order=W-1&sku=KETTLE-1&qty=1&price=30.00";
    static final String CSV = "A-77,MUG-1,2,1600";
    static final String JSON = "{\"ref\":\"B-9\",\"item\":\"TEAPOT-1\",\"count\":1,\"total\":25.00,"
            + "\"giftNote\":\"Happy birthday, Mum\"}";
    static final String XML = "<order id=\"C-5\"><line sku=\"KETTLE-1\" qty=\"1\" price=\"30.00\"/></order>";

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        Warehouse warehouse = new Warehouse();
        try (CamelContext camel = new DefaultCamelContext()) {
            camel.addRoutes(new ShopRoutes(warehouse));
            camel.start();
            ProducerTemplate send = camel.createProducerTemplate();

            out.add("ONE. Send a marketplace's JSON straight to the warehouse route.");
            try {
                send.sendBody("direct:warehouse", JSON);
            } catch (CamelExecutionException e) {
                out.add("  Camel refuses: " + rootCause(e));
            }
            out.add("  the warehouse route converts to OrderMessage first, and there is no way from raw JSON");

            out.add("");
            out.add("TWO. One translator route per format, using Camel's data formats.");
            send.sendBody("direct:translate-web", WEB);
            send.sendBody("direct:translate-csv", CSV);
            send.sendBody("direct:translate-json", JSON);
            out.add("  web form (key=value, split by hand)   -> " + warehouse.picks().get(0));
            out.add("  CSV (unmarshal().csv())               -> " + warehouse.picks().get(1));
            out.add("  JSON (unmarshal().json(Jackson))      -> " + warehouse.picks().get(2));

            out.add("");
            out.add("THREE. The normalizer: one inbox, format recognised, toD to the translator.");
            warehouse.picks().clear();
            for (String order : List.of(CSV, JSON, WEB)) {
                send.sendBody("direct:inbox", order);
            }
            for (String pick : warehouse.picks()) {
                out.add("  " + pick);
            }
            out.add("  routes running: " + camel.getRoutes().size() + " (normalizer, 3 translators, warehouse)");

            out.add("");
            out.add("FOUR. Marketplace C sends XML.");
            try {
                send.sendBody("direct:inbox", XML);
            } catch (CamelExecutionException e) {
                out.add("  before: " + rootCause(e));
            }
            camel.addRoutes(ShopRoutes.xmlTranslator());
            warehouse.picks().clear();
            send.sendBody("direct:inbox", XML);
            out.add("  after adding one route, translate-xml: " + warehouse.picks().get(0));
            out.add("  the normalizer and the warehouse routes were not changed");

            out.add("");
            out.add("FIVE. The bill.");
            warehouse.picks().clear();
            out.add("  marketplace B's gift note still does not survive: the canonical order has no room for it");
            int jars = System.getProperty("java.class.path").split(java.io.File.pathSeparator).length;
            out.add("  and the program now carries " + (jars > 20 ? "more than 20" : "about " + jars)
                    + " library files, against none for the plain version");
        }
        return out;
    }

    private static String rootCause(Throwable e) {
        Throwable t = e;
        while (t.getCause() != null) {
            t = t.getCause();
        }
        String name = t.getClass().getSimpleName();
        if (name.equals("NoTypeConversionAvailableException")) {
            return "no type converter from String to OrderMessage";
        }
        if (name.equals("DirectConsumerNotAvailableException")) {
            return "no consumers available on endpoint direct://translate-xml";
        }
        return name + ": " + t.getMessage();
    }

    private CamelTranslatorDemo() {
    }
}
