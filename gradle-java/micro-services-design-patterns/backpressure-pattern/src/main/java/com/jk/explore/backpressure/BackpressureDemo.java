package com.jk.explore.backpressure;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * The five acts: no backpressure, a bounded buffer, asking for what you can handle, keeping only the latest, and the bill.
 */
public final class BackpressureDemo {

    static final int PRODUCTS = 10_000;

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. The supplier sends as fast as it can.");
        FeedSimulation.Result r1 = FeedSimulation.run(PRODUCTS, 0, 10);
        out.add("  supplier: " + FeedSimulation.SUPPLIER_PER_SECOND + " products a second; indexer: "
                + FeedSimulation.INDEXER_PER_SECOND + " a second");
        out.add("  after " + r1.seconds() + " s: " + r1.indexed() + " indexed, " + r1.finalWaiting()
                + " waiting in memory, and growing by 900 a second");
        out.add("  a bigger feed, or a slower indexer, and the service runs out of memory");

        out.add("");
        out.add("TWO. A bounded buffer: when it is full, the producer waits.");
        FeedSimulation.Result r2 = FeedSimulation.run(PRODUCTS, 500, 1000);
        out.add("  buffer of 500: never more than " + r2.maxWaiting() + " waiting; all " + r2.indexed()
                + " indexed in " + r2.seconds() + " s");
        out.add("  the supplier was slowed to the indexer's pace");

        out.add("");
        out.add("THREE. The consumer asks for what it can handle.");
        PullPublisher feed = new PullPublisher(PRODUCTS);
        Indexer indexer = new Indexer(10);
        feed.subscribe(indexer);
        out.add("  with Java's Flow interfaces, the indexer requests 10 at a time");
        out.add("  indexed " + indexer.indexed() + "; at most " + feed.maxOutstanding()
                + " products were ever in flight, and nothing was sent unasked");

        out.add("");
        out.add("FOUR. When only the latest matters, drop the rest.");
        Conflator stock = new Conflator();
        for (int i = 0; i < 1000; i++) {
            stock.offer("SKU-" + (i % 10), 1000 - i);
        }
        Map<String, Integer> latest = stock.drain();
        out.add("  1000 stock-level updates for 10 products: " + latest.size() + " delivered, the latest for each");
        out.add("  SKU-3 now: " + latest.get("SKU-3"));

        out.add("");
        out.add("FIVE. The bill: the waiting moves upstream, or data is dropped.");
        out.add("  the supplier's 10,000-product feed took " + r2.seconds() + " s instead of 10: it must cope with being slowed");
        out.add("  and dropping only works for data where the latest value is all that matters");
        return out;
    }

    private BackpressureDemo() {
    }
}
