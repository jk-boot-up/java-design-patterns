package com.jk.explore.splitteraggregator;

import java.util.List;
import java.util.Optional;

public class SplitterAggregatorDemo {

    static final List<String> LINES = List.of("2 x MUG-BLUE (aisle 3)", "1 x ESP-001 (aisle 9)", "5 x TEA-050 (aisle 1)");

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. One message, one picker.");
        System.out.println("  an order of " + LINES.size() + " lines is picked by one person, one line after another: " + LINES.size() + " steps of work, in a row.");
        System.out.println("  the aisles are far apart, and the other pickers stand idle.");
    }

    private static void two() {
        System.out.println("TWO. Split it.");
        for (Part p : Splitter.split("ORD-1", LINES)) {
            System.out.println("  " + p.orderId() + " part " + p.index() + " of " + p.total() + ": " + p.content());
        }
        System.out.println("  each part carries the order's id, and its place. that is what lets it be put back.");
    }

    private static void three() {
        System.out.println("THREE. The parts finish in any order.");
        List<Part> parts = Splitter.split("ORD-1", LINES);
        int[] finishOrder = {3, 1, 2};
        StringBuilder sb = new StringBuilder();
        for (int i : finishOrder) {
            sb.append(parts.get(i - 1).index()).append(" ");
        }
        System.out.println("  suppose the three pickers finish in the order: " + sb.toString().trim() + ".");
        System.out.println("  nothing guarantees they come back in the order they went.");
    }

    private static void four() {
        System.out.println("FOUR. Gather them by the id.");
        Aggregator aggregator = new Aggregator(new Clock(), 30);
        List<Part> parts = Splitter.split("ORD-1", LINES);
        for (int i : new int[]{3, 1, 2}) {
            Optional<Aggregator.Result> r = aggregator.accept(parts.get(i - 1));
            System.out.println("  part " + i + " arrives. " + r.map(x -> "complete: " + x.contents()).orElse("waiting for the rest") + ".");
        }
        System.out.println("  the order came back together, in its original line order, from parts that arrived out of order.");
    }

    private static void five() {
        System.out.println("FIVE. A part never arrives.");
        Clock clock = new Clock();
        Aggregator aggregator = new Aggregator(clock, 30);
        List<Part> parts = Splitter.split("ORD-1", LINES);
        aggregator.accept(parts.get(0));
        aggregator.accept(parts.get(2));
        System.out.println("  parts 1 and 3 arrive. part 2's picker has gone home. open orders: " + aggregator.openOrders() + ".");
        clock.advance(29);
        System.out.println("  after 29 minutes: expired " + aggregator.expire().size() + ".");
        clock.advance(1);
        Aggregator.Result partial = aggregator.expire().get(0);
        System.out.println("  after 30 minutes the aggregator gives up: " + partial.contents().size() + " of 3 lines, missing part " + partial.missing() + ", complete: " + partial.complete() + ".");
        System.out.println("  without a timeout it would wait for ever, and the customer would too.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        Aggregator aggregator = new Aggregator(new Clock(), 30);
        for (int i = 0; i < 1000; i++) {
            List<Part> parts = Splitter.split("ORD-" + i, LINES);
            aggregator.accept(parts.get(0));
            aggregator.accept(parts.get(1));
        }
        System.out.println("  1000 orders each missing one part: " + aggregator.openOrders() + " orders held in memory, waiting.");
        Aggregator dup = new Aggregator(new Clock(), 30);
        List<Part> parts = Splitter.split("ORD-1", LINES);
        dup.accept(parts.get(0));
        dup.accept(parts.get(0));
        System.out.println("  a part delivered twice: counted once, and " + dup.duplicates() + " duplicate noted. without that, an order could complete with a line twice.");
        System.out.println("  and two orders with the same id would be mixed into one. the id that ties the parts together has to be unique.");
    }
}
