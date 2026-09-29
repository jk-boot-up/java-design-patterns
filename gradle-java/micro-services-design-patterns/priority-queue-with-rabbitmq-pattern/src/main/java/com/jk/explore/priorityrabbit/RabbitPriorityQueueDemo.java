package com.jk.explore.priorityrabbit;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts, against a real RabbitMQ broker started and stopped by this program.
 * Minutes are counted, not waited for: each minute the pickers take ten orders.
 */
public final class RabbitPriorityQueueDemo {

    public static void main(String[] args) throws Exception {
        if (!Broker.containerRuntimeAvailable()) {
            System.out.println(Broker.NO_RUNTIME_ADVICE);
            return;
        }
        for (String line : run()) {
            System.out.println(line);
        }
    }

    static String clock(int minute) {
        return String.format("9:%02d", minute);
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        try (Broker broker = new Broker()) {
            try {
                broker.start();
            } catch (RuntimeException e) {
                out.add(Broker.WOULD_NOT_START_ADVICE);
                return out;
            }
            try (Warehouse w = new Warehouse(broker)) {

                out.add("ONE. An ordinary queue: first in, first out.");
                w.declare("orders", false);
                w.place("orders", "STD", 100, Warehouse.STANDARD);
                w.place("orders", "SAME", 5, Warehouse.SAME_DAY);
                w.settle("orders", 105);
                int m = w.minuteLastPicked("orders", "SAME", 5, 10);
                out.add("  100 standard orders, then 5 same-day; pickers take 10 a minute from 9:00");
                out.add("  the last same-day order is picked at " + clock(m) + "; the van left at 9:05");

                out.add("");
                out.add("TWO. A RabbitMQ priority queue: x-max-priority 10, same-day sent with priority 9.");
                w.declare("orders-p", true);
                w.place("orders-p", "STD", 100, Warehouse.STANDARD);
                w.place("orders-p", "SAME", 5, Warehouse.SAME_DAY);
                w.settle("orders-p", 105);
                m = w.minuteLastPicked("orders-p", "SAME", 5, 10);
                out.add("  all 5 same-day orders picked by " + clock(m) + ", in time for the van");

                out.add("");
                out.add("THREE. A flood of standard orders.");
                w.declare("orders-p", true);
                w.place("orders-p", "STD", 1000, Warehouse.STANDARD);
                w.place("orders-p", "SAME", 5, Warehouse.SAME_DAY);
                w.settle("orders-p", 1005);
                m = w.minuteLastPicked("orders-p", "SAME", 5, 10);
                out.add("  1000 standard orders ahead of them: same-day still picked by " + clock(m));

                out.add("");
                out.add("FOUR. Priority only reorders what is still waiting on the queue.");
                w.declare("orders-p", true);
                w.place("orders-p", "STD", 100, Warehouse.STANDARD);
                w.settle("orders-p", 100);
                List<String> unlimited = w.subscribe("orders-p", 0);
                Poll.until("100 pushed to the handheld", () -> unlimited.size() == 100);
                w.place("orders-p", "SAME", 5, Warehouse.SAME_DAY);
                Poll.until("the same-day orders pushed too", () -> unlimited.size() == 105);
                out.add("  a handheld with no prefetch limit had all 100 standard orders pushed to it already");
                out.add("  the same-day orders arrive and join the back: positions " + (unlimited.indexOf("SAME-1") + 1)
                        + " to " + (unlimited.indexOf("SAME-5") + 1) + " of " + unlimited.size());
                w.declare("orders-p", true);
                w.place("orders-p", "STD", 100, Warehouse.STANDARD);
                w.settle("orders-p", 100);
                List<String> limited = w.subscribe("orders-p", 1);
                Poll.until("one pushed", () -> limited.size() == 1);
                w.place("orders-p", "SAME", 5, Warehouse.SAME_DAY);
                w.settle("orders-p", 104);
                out.add("  with prefetch 1, the next order the queue will hand out: " + w.pickMinute("orders-p", 1));

                out.add("");
                out.add("FIVE. The bill: starvation, and no reserved share.");
                w.declare("orders-p", true);
                int standardPicked = 0;
                for (int minute = 1; minute <= 10; minute++) {
                    w.place("orders-p", "SAME" + minute, 12, Warehouse.SAME_DAY);
                    if (minute == 1) {
                        w.place("orders-p", "STD", 20, Warehouse.STANDARD);
                    }
                    w.settle("orders-p", expectedAfter(minute));
                    for (String o : w.pickMinute("orders-p", 10)) {
                        if (o.startsWith("STD-")) {
                            standardPicked++;
                        }
                    }
                }
                out.add("  12 same-day orders a minute, 10 picks: standard orders picked in 10 minutes: " + standardPicked + " of 20");
                w.declare("standard", false);
                w.declare("same-day", false);
                w.place("standard", "STD", 20, Warehouse.STANDARD);
                w.settle("standard", 20);
                int reserved = 0;
                for (int minute = 1; minute <= 10; minute++) {
                    reserved += w.pickMinute("standard", 2).size();
                }
                out.add("  RabbitMQ has no reserved share; two queues, 2 picks a minute kept for standard: " + reserved + " of 20");
            }
        }
        return out;
    }

    /** Orders waiting just before the pickers start minute {@code minute}. */
    private static int expectedAfter(int minute) {
        int arrived = 12 * minute + 20;
        int picked = 10 * (minute - 1);
        return arrived - picked;
    }

    private RabbitPriorityQueueDemo() {
    }
}
