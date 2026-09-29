package com.jk.explore.wiretapcamel;

import java.util.ArrayList;
import java.util.List;
import org.apache.camel.CamelContext;
import org.apache.camel.ProducerTemplate;
import org.apache.camel.impl.DefaultCamelContext;

/**
 * The five acts, with Apache Camel's wireTap().
 */
public final class CamelWireTapDemo {

    static List<PaymentMessage> payments() {
        return List.of(
                new PaymentMessage("CHARGE", "ORD-1", 6344, "4929123412341234"),
                new PaymentMessage("CHARGE", "ORD-2", 1999, "4929555566667777"),
                new PaymentMessage("REFUND", "ORD-1", 3000, "4929123412341234"),
                new PaymentMessage("CHARGE", "ORD-3", 499, "4929000011112222"));
    }

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();

        out.add("ONE. wireTap(\"direct:audit\") on the payments route.");
        PaymentService payment = new PaymentService();
        Audit audit = new Audit();
        List<PaymentMessage> sent = payments();
        try (CamelContext camel = start(new ShopRoutes(payment, audit, false))) {
            ProducerTemplate send = camel.createProducerTemplate();
            sent.forEach(m -> send.sendBody("direct:payments", m));
            audit.awaitLines(4, 5000);
        }
        audit.lines().stream().sorted().forEach(l -> out.add("  " + l));
        out.add("  " + audit.lines().size() + " of 4 copied, the refund included; payment handled " + payment.handled().size());
        out.add("  neither checkout nor the payment service was changed");

        out.add("");
        out.add("TWO. The tap was handed the same object, not a copy.");
        out.add("  checkout's own ORD-1 message now says: " + sent.get(0));
        out.add("  the audit's masking changed the real payment instruction");

        out.add("");
        out.add("THREE. onPrepare(copy): the tap gets its own object.");
        payment = new PaymentService();
        audit = new Audit();
        sent = payments();
        try (CamelContext camel = start(new ShopRoutes(payment, audit, true))) {
            ProducerTemplate send = camel.createProducerTemplate();
            sent.forEach(m -> send.sendBody("direct:payments", m));
            audit.awaitLines(4, 5000);

            out.add("  audit lines: " + audit.lines().size() + "; checkout's ORD-1 message still says: " + sent.get(0));

            out.add("");
            out.add("FOUR. The audit route is stopped.");
            camel.getRouteController().stopRoute("audit");
            send.sendBody("direct:payments", new PaymentMessage("CHARGE", "ORD-4", 1200, "4929999988887777"));
            out.add("  ORD-4: " + payment.handled().get(payment.handled().size() - 1)
                    + "; the failed copy did not reach checkout or the payment service");
            camel.getRouteController().startRoute("audit");

            out.add("");
            out.add("FIVE. The bill: a slow audit, and copies still in flight.");
            audit.setDelayMillis(100);
            int before = audit.lines().size();
            long start = System.nanoTime();
            payments().forEach(m -> send.sendBody("direct:payments", m));
            long millis = (System.nanoTime() - start) / 1_000_000;
            out.add("  an audit taking 100 ms per copy: 4 payments took " + (millis < 300 ? "under 0.3 s, not the 0.4 s four slow copies add up to" : "over 0.3 s")
                    + ", because the tap runs on its own thread");
            boolean caughtUp = audit.awaitLines(before + 4, 5000);
            out.add("  but the audit lagged behind, and caught up only later: " + (caughtUp ? "4 of 4" : "not yet"));
            out.add("  copies waiting in memory are lost if the program stops: for a real audit, tap to a durable queue");
        }
        return out;
    }

    private static CamelContext start(ShopRoutes routes) throws Exception {
        CamelContext camel = new DefaultCamelContext();
        camel.addRoutes(routes);
        camel.start();
        return camel;
    }

    private CamelWireTapDemo() {
    }
}
