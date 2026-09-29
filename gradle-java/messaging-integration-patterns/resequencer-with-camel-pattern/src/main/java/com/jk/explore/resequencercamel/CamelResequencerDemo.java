package com.jk.explore.resequencercamel;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.apache.camel.CamelContext;
import org.apache.camel.ProducerTemplate;
import org.apache.camel.impl.DefaultCamelContext;

/**
 * The five acts, with Apache Camel's resequence() step.
 */
public final class CamelResequencerDemo {

    static final String[] STATUS = {"", "PLACED", "PAID", "PACKED", "SHIPPED", "DELIVERED"};
    static final int[] ARRIVAL = {1, 3, 2, 5, 4};

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();

        out.add("ONE. Status updates applied as they arrive.");
        OrderPage page = new OrderPage();
        try (CamelContext camel = start(page, 5_000)) {
            ProducerTemplate send = camel.createProducerTemplate();
            for (int n : ARRIVAL) {
                send(send, "direct:as-they-come", "ORD-1", n);
            }
        }
        out.add("  arrival order: [#1, #3, #2, #5, #4]");
        out.add("  the customer saw: " + page.shown());
        out.add("  final status: " + page.latest() + ", but the parcel was DELIVERED");

        out.add("");
        out.add("TWO. resequence(header(\"seq\")).stream().timeout(300)");
        page = new OrderPage();
        try (CamelContext camel = start(page, 300)) {
            ProducerTemplate send = camel.createProducerTemplate();
            long start = System.nanoTime();
            for (int n : ARRIVAL) {
                send(send, "direct:stream", "ORD-1", n);
            }
            page.await(1, 5_000);
            long firstMillis = (System.nanoTime() - start) / 1_000_000;
            page.await(5, 5_000);
            out.add("  the customer saw: " + page.shown());
            out.add("  final status: " + page.latest());
            out.add("  the first update appeared only after " + (firstMillis >= 250 ? "about 0.3 s" : "no wait")
                    + ": Camel cannot know #1 is the first, so it waits one timeout");
        }

        out.add("");
        out.add("THREE. Batch mode: collect 5, sort, release together.");
        page = new OrderPage();
        try (CamelContext camel = start(page, 300)) {
            ProducerTemplate send = camel.createProducerTemplate();
            for (int i = 0; i < 4; i++) {
                send(send, "direct:batch", "ORD-1", ARRIVAL[i]);
            }
            out.add("  after 4 arrivals the customer sees: " + page.shown());
            send(send, "direct:batch", "ORD-1", ARRIVAL[4]);
            page.await(5, 5_000);
            out.add("  after the 5th: " + page.shown());
            out.add("  batch mode never releases out of order, but nothing shows until the batch is full");
        }

        out.add("");
        out.add("FOUR. Two orders interleaved: batch mode sorts by order, then number.");
        page = new OrderPage();
        try (CamelContext camel = start(page, 5_000)) {
            ProducerTemplate send = camel.createProducerTemplate();
            send(send, "direct:batch", "ORD-3", 2);
            send(send, "direct:batch", "ORD-2", 2);
            send(send, "direct:batch", "ORD-3", 1);
            send(send, "direct:batch", "ORD-2", 1);
            send(send, "direct:batch", "ORD-3", 3);
            page.await(5, 5_000);
        }
        out.add("  arrivals: ORD-3#2, ORD-2#2, ORD-3#1, ORD-2#1, ORD-3#3");
        out.add("  released: " + page.shown());
        out.add("  the stream mode keeps one sequence only; per-order sequences need batch mode or a key");

        out.add("");
        out.add("FIVE. The bill: #3 is lost, and the gap times out after 0.5 s.");
        page = new OrderPage();
        try (CamelContext camel = start(page, 500)) {
            ProducerTemplate send = camel.createProducerTemplate();
            send(send, "direct:stream", "ORD-1", 1);
            send(send, "direct:stream", "ORD-1", 2);
            page.await(2, 5_000);
            long start = System.nanoTime();
            send(send, "direct:stream", "ORD-1", 4);
            send(send, "direct:stream", "ORD-1", 5);
            out.add("  #4 and #5 arrive: the page still says " + page.latest() + " while they wait for #3");
            page.await(4, 5_000);
            long millis = (System.nanoTime() - start) / 1_000_000;
            out.add("  " + (millis >= 400 ? "after about half a second" : "at once")
                    + " the gap is given up: the page says " + page.latest());
            out.add("  a short timeout loses #3 quickly; a long one leaves the customer on PAID for longer");
        }
        return out;
    }
    private static void send(ProducerTemplate send, String uri, String order, long seq) {
        String body = order.equals("ORD-1") ? STATUS[(int) seq] : order + " " + STATUS[(int) seq];
        send.sendBodyAndHeaders(uri, body, Map.of("seq", seq, "order", order));
    }

    private static CamelContext start(OrderPage page, long gapTimeoutMillis) throws Exception {
        CamelContext camel = new DefaultCamelContext();
        camel.addRoutes(new ShopRoutes(page, gapTimeoutMillis));
        camel.start();
        return camel;
    }

    private CamelResequencerDemo() {
    }
}
