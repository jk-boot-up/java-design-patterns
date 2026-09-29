package com.jk.explore.priorityqueue;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * The five acts: one first-come queue, a priority queue, a flood of standard orders, starvation and a reserved share, and the bill.
 */
public final class PriorityQueueDemo {

    static final int CUT_OFF = 5;

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** 100 standard orders at minute 0, then 5 same-day orders at minute 1. */
    static List<Order> morning(int standard) {
        List<Order> list = new ArrayList<>();
        long seq = 0;
        for (int i = 1; i <= standard; i++) {
            list.add(new Order("STD-" + i, false, 0, seq++));
        }
        for (int i = 1; i <= 5; i++) {
            list.add(new Order("SAME-" + i, true, 1, seq++));
        }
        return list;
    }

    static int lastSameDay(Map<String, Integer> picked) {
        return picked.entrySet().stream().filter(e -> e.getKey().startsWith("SAME")).mapToInt(Map.Entry::getValue).max().orElse(-1);
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. One queue, first come first served.");
        Map<String, Integer> fifo = Picking.run(Picking.fifo(), morning(100), 20, 0);
        int last1 = lastSameDay(fifo);
        out.add("  100 standard orders arrive at 9:00; 5 same-day orders at 9:01; the van leaves at 9:0" + CUT_OFF);
        out.add("  pickers do 10 a minute: the last same-day order is picked at 9:" + String.format("%02d", last1)
                + (last1 > CUT_OFF ? ", after the van has gone" : ""));

        out.add("");
        out.add("TWO. A priority queue: same-day first.");
        Map<String, Integer> prio = Picking.run(Picking.priority(), morning(100), 20, 0);
        out.add("  all 5 same-day orders picked by 9:" + String.format("%02d", lastSameDay(prio)) + ", in time for the van");
        out.add("  standard orders carry on straight after");

        out.add("");
        out.add("THREE. A flood of standard orders makes no difference.");
        Map<String, Integer> flood = Picking.run(Picking.priority(), morning(1000), 20, 0);
        out.add("  1000 standard orders ahead of them: same-day still picked by 9:" + String.format("%02d", lastSameDay(flood)));

        out.add("");
        out.add("FOUR. Too many urgent orders starve the rest.");
        List<Order> rush = new ArrayList<>();
        long seq = 0;
        for (int i = 1; i <= 20; i++) {
            rush.add(new Order("STD-" + i, false, 0, seq++));
        }
        for (int minute = 0; minute < 10; minute++) {
            for (int i = 1; i <= 12; i++) {
                rush.add(new Order("SAME-" + minute + "-" + i, true, minute, seq++));
            }
        }
        long strict = Picking.run(Picking.priority(), rush, 10, 0).keySet().stream().filter(k -> k.startsWith("STD")).count();
        out.add("  12 same-day orders a minute, pickers do 10: standard orders picked in 10 minutes: " + strict + " of 20");
        long shared = Picking.run(Picking.priority(), rush, 10, 2).keySet().stream().filter(k -> k.startsWith("STD")).count();
        out.add("  keep 2 picks a minute for the oldest standard orders: " + shared + " of 20 picked");

        out.add("");
        out.add("FIVE. The bill: if everything is urgent, nothing is.");
        out.add("  marketplace sellers learn that same-day jumps the queue, and mark every order same-day");
        out.add("  priorities need rules about who may set them, and more queues and settings to watch");
        return out;
    }

    private PriorityQueueDemo() {
    }
}
