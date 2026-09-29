package com.jk.explore.contentenricher;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * The five acts: the thin message, every receiver looking it up, the enricher, a missing customer, and the bill.
 */
public final class ContentEnricherDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    static CustomerDirectory directory() {
        return new CustomerDirectory()
                .add(new Customer("C-17", "Priya Shah", "4 Mill Lane, Leeds", "GOLD"))
                .add(new Customer("C-42", "Tom Reed", "9 Park Road, Bath", "STANDARD"));
    }

    static List<OrderPlaced> orders() {
        return List.of(
                new OrderPlaced("ORD-1", "C-17", List.of("kettle")),
                new OrderPlaced("ORD-2", "C-42", List.of("mug", "tea")),
                new OrderPlaced("ORD-3", "C-17", List.of("toaster")));
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. Checkout sends a thin message.");
        OrderPlaced first = orders().get(0);
        out.add("  " + first);
        out.add("  it says who ordered only as C-17: no name, no address, no loyalty tier");

        out.add("");
        out.add("TWO. Without an enricher, every receiver looks the customer up.");
        CustomerDirectory d1 = directory();
        for (OrderPlaced o : orders()) {
            Receivers.packThin(o, d1);
            Receivers.emailThin(o, d1);
        }
        out.add("  3 orders, 2 receivers: " + d1.lookups() + " calls to the customer service");
        d1.setUp(false);
        try {
            Receivers.packThin(orders().get(0), d1);
        } catch (IllegalStateException e) {
            out.add("  customer service goes down: the warehouse stops packing, " + e.getMessage());
        }

        out.add("");
        out.add("THREE. The enricher adds the details once, on the way.");
        CustomerDirectory d2 = directory();
        ContentEnricher enricher = new ContentEnricher(d2, true);
        List<EnrichedOrder> enriched = new ArrayList<>();
        for (OrderPlaced o : orders()) {
            enricher.enrich(o).ifPresent(enriched::add);
        }
        out.add("  " + enriched.get(0));
        out.add("  message grew from " + first.size() + " to " + enriched.get(0).size() + " characters");
        out.add("  3 orders, with a cache: " + d2.lookups() + " calls to the customer service");
        d2.setUp(false);
        out.add("  customer service goes down: " + Receivers.pack(enriched.get(0))
                + ", " + Receivers.email(enriched.get(0)));

        out.add("");
        out.add("FOUR. A customer who cannot be found.");
        ContentEnricher e2 = new ContentEnricher(directory(), true);
        Optional<EnrichedOrder> lost = e2.enrich(new OrderPlaced("ORD-4", "C-99", List.of("lamp")));
        out.add("  ORD-4 for C-99 enriched: " + lost.isPresent());
        out.add("  sent to the problem list: " + e2.problems());

        out.add("");
        out.add("FIVE. The bill: the details are a copy, taken at one moment.");
        CustomerDirectory d3 = directory();
        EnrichedOrder copy = new ContentEnricher(d3, false).enrich(first).orElseThrow();
        d3.moveHouse("C-17", "12 High Street, York");
        out.add("  Priya moves house after the order was enriched");
        out.add("  the message still says: " + copy.address());
        out.add("  and every enriched message is bigger, for every receiver, whether it needs the details or not");
        return out;
    }

    private ContentEnricherDemo() {
    }
}
