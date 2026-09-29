package com.jk.explore.pollingconsumer;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

/**
 * The five acts: orders pushed at the printer, a polling consumer, pausing, how often to poll, and the bill.
 */
public final class PollingConsumerDemo {

    static final int BURST = 50;

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    static Deque<String> burst(int n) {
        Deque<String> q = new ArrayDeque<>();
        for (int i = 1; i <= n; i++) {
            q.add("ORD-" + i);
        }
        return q;
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. Orders pushed at the printer as they arrive.");
        LabelPrinter pushed = new LabelPrinter();
        int refused = 0;
        for (String order : burst(BURST)) {
            if (!pushed.push(order)) {
                refused++;
            }
        }
        out.add("  a burst of " + BURST + " orders; the printer's buffer holds " + LabelPrinter.BUFFER);
        out.add("  printed: " + pushed.printed() + ", refused: " + refused + " (printer busy)");

        out.add("");
        out.add("TWO. A polling consumer takes orders when it is ready.");
        Deque<String> queue = burst(BURST);
        LabelPrinter printer = new LabelPrinter();
        PollingConsumer consumer = new PollingConsumer(queue, printer);
        int ticks = 0;
        while (!queue.isEmpty()) {
            consumer.tick();
            ticks++;
        }
        out.add("  every tick it asks the queue for up to " + LabelPrinter.PER_TICK);
        out.add("  printed: " + printer.printed() + " of " + BURST + " in " + ticks + " ticks (" + ticks / 10.0 + " s); refused: 0");

        out.add("");
        out.add("THREE. Pausing is simply not polling.");
        Deque<String> q3 = burst(20);
        LabelPrinter p3 = new LabelPrinter();
        PollingConsumer c3 = new PollingConsumer(q3, p3);
        c3.tick();
        c3.pause();
        for (int i = 0; i < 30; i++) {
            c3.tick();
        }
        out.add("  paper runs out after one tick; the printer stops polling for 3 seconds");
        out.add("  printed " + p3.printed() + ", waiting safely in the queue: " + q3.size());
        c3.resume();
        while (!q3.isEmpty()) {
            c3.tick();
        }
        out.add("  paper loaded, polling resumes: printed " + p3.printed() + " of 20, none lost");

        out.add("");
        out.add("FOUR. How often to poll when nothing is happening?");
        PollingConsumer idle = new PollingConsumer(new ArrayDeque<>(), new LabelPrinter());
        for (int i = 0; i < 600; i++) {
            idle.tick();
        }
        out.add("  a quiet minute, asking every tenth of a second: " + idle.polls() + " polls, " + idle.emptyPolls() + " empty");
        out.add("  long polling (\"wait up to 20 s for something to arrive\"): 3 requests for the same quiet minute");

        out.add("");
        out.add("FIVE. The bill: a message waits for the next poll.");
        out.add("  an order arriving just after a poll waits until the next one: up to a whole interval");
        out.add("  poll often and waste requests, or poll rarely and add waiting; long polling is the usual middle");
        return out;
    }

    private PollingConsumerDemo() {
    }
}
