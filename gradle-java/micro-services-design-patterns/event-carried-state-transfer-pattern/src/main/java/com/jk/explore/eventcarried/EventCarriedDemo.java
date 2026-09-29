package com.jk.explore.eventcarried;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: thin events with call-backs, events that carry the address, the delay window,
 * events out of order, and the bill.
 */
public final class EventCarriedDemo {

    static final int ORDERS = 100;

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. A thin event, and a call back for the address.");
        CustomerService customers = new CustomerService();
        for (int c = 1; c <= 10; c++) {
            customers.move("C" + c, new Address(c + " High Street", "Leeds"));
        }
        CallbackShipping callback = new CallbackShipping(customers);
        callback.on(new Events.CustomerChanged("C1"));
        out.add("  " + ORDERS + " labels: " + printed(callback, ORDERS) + " printed, "
                + customers.lookups() + " calls to the customer service");
        customers.setUp(false);
        out.add("  customer service down: " + printed(callback, ORDERS) + " of " + ORDERS + " labels printed");
        customers.setUp(true);

        out.add("");
        out.add("TWO. The event carries the new address.");
        CustomerService owner = new CustomerService();
        ReplicaShipping shipping = new ReplicaShipping(true);
        for (int c = 1; c <= 10; c++) {
            shipping.on(owner.move("C" + c, new Address(c + " High Street", "Leeds")));
        }
        out.add("  shipping keeps its own copy of " + shipping.copies() + " addresses");
        out.add("  " + ORDERS + " labels: " + printed(shipping, ORDERS) + " printed, " + owner.lookups()
                + " calls to the customer service");
        owner.setUp(false);
        out.add("  customer service down: " + printed(shipping, ORDERS) + " of " + ORDERS + " labels still printed");

        out.add("");
        out.add("THREE. The copy lags behind for a moment.");
        Events.AddressChanged moved = owner.move("C1", new Address("9 Mill Lane", "York"));
        out.add("  C1 moves to York; the event is still on its way");
        out.add("  label printed now:  " + shipping.label("ORD-1", "C1"));
        shipping.on(moved);
        out.add("  after the event:    " + shipping.label("ORD-1", "C1"));

        out.add("");
        out.add("FOUR. Two moves, arriving in the wrong order.");
        Events.AddressChanged first = owner.move("C2", new Address("1 Park Road", "Hull"));
        Events.AddressChanged second = owner.move("C2", new Address("4 Quay Street", "Bristol"));
        ReplicaShipping naive = new ReplicaShipping(false);
        naive.on(second);
        naive.on(first);
        shipping.on(second);
        shipping.on(first);
        out.add("  without versions: " + naive.label("ORD-2", "C2") + "  (the older address wins)");
        out.add("  with versions:    " + shipping.label("ORD-2", "C2") + "  (version " + first.version()
                + " ignored after " + second.version() + ")");

        out.add("");
        out.add("FIVE. The bill: copies everywhere.");
        out.add("  shipping, invoicing and marketing each keep their own copy of every address");
        out.add("  bigger events, copies that are briefly stale, and personal data in more places");
        return out;
    }

    private static int printed(CallbackShipping shipping, int orders) {
        int n = 0;
        for (int i = 0; i < orders; i++) {
            if (shipping.label("ORD-" + i, "C" + (i % 10 + 1)) != null) {
                n++;
            }
        }
        return n;
    }

    private static int printed(ReplicaShipping shipping, int orders) {
        int n = 0;
        for (int i = 0; i < orders; i++) {
            if (shipping.label("ORD-" + i, "C" + (i % 10 + 1)) != null) {
                n++;
            }
        }
        return n;
    }

    private EventCarriedDemo() {
    }
}
