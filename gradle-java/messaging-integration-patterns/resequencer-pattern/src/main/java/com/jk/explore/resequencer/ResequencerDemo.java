package com.jk.explore.resequencer;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: updates applied as they arrive, a resequencer, holding and releasing, several orders at once, and the bill.
 */
public final class ResequencerDemo {

    static final String[] STATUSES = {"", "PLACED", "PAID", "PACKED", "SHIPPED", "DELIVERED"};

    static StatusUpdate u(String order, int seq) {
        return new StatusUpdate(order, seq, STATUSES[seq]);
    }

    /** Parallel processing upstream delivered them in this order. */
    static final List<StatusUpdate> ARRIVALS = List.of(u("ORD-1", 1), u("ORD-1", 3), u("ORD-1", 2), u("ORD-1", 5), u("ORD-1", 4));

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. Status updates applied as they arrive.");
        out.add("  arrival order: " + ARRIVALS.stream().map(s -> "#" + s.seq()).toList());
        OrderPage page1 = new OrderPage();
        ARRIVALS.forEach(page1::apply);
        out.add("  the customer saw: " + page1.shown().stream().map(s -> s.split(" ")[1]).toList());
        out.add("  final status: " + page1.status("ORD-1") + ", but the parcel was DELIVERED");

        out.add("");
        out.add("TWO. A resequencer puts them back in order.");
        OrderPage page2 = new OrderPage();
        Resequencer rs = new Resequencer(page2::apply, 10);
        ARRIVALS.forEach(rs::accept);
        out.add("  the customer saw: " + page2.shown().stream().map(s -> s.split(" ")[1]).toList());
        out.add("  final status: " + page2.status("ORD-1"));

        out.add("");
        out.add("THREE. Early messages wait; late ones release them.");
        rs.trace().forEach(t -> out.add("  " + t));

        out.add("");
        out.add("FOUR. Each order has its own sequence.");
        OrderPage page4 = new OrderPage();
        Resequencer rs4 = new Resequencer(page4::apply, 10);
        List.of(u("ORD-2", 2), u("ORD-3", 1), u("ORD-2", 1), u("ORD-3", 3), u("ORD-3", 2)).forEach(rs4::accept);
        out.add("  interleaved arrivals for two orders, each released in its own order:");
        out.add("  " + page4.shown());

        out.add("");
        out.add("FIVE. The bill: a lost message holds up everything behind it.");
        OrderPage page5 = new OrderPage();
        Resequencer rs5 = new Resequencer(page5::apply, 2);
        rs5.accept(u("ORD-4", 1));
        rs5.accept(u("ORD-4", 2));
        rs5.accept(u("ORD-4", 4));
        out.add("  #3 PACKED is lost; #4 SHIPPED arrives: page still says " + page5.status("ORD-4")
                + ", holding " + rs5.holding("ORD-4"));
        rs5.accept(u("ORD-4", 5));
        out.add("  #5 DELIVERED arrives; two now wait, so the gap is given up on: page says " + page5.status("ORD-4"));
        out.add("  without a limit, the page would wait for #3 for ever; with one, #3 is simply missed");
        return out;
    }

    private ResequencerDemo() {
    }
}
