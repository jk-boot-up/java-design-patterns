package com.jk.explore.priorityqueue;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Queue;

/**
 * The warehouse pickers: they pick 10 orders a minute from a queue. The queue decides which 10.
 */
public final class Picking {

    public static final int PER_MINUTE = 10;

    /** Without the pattern: first in, first out. */
    public static Queue<Order> fifo() {
        return new ArrayDeque<>();
    }

    /** The pattern: same-day first, then oldest first. */
    public static Queue<Order> priority() {
        return new PriorityQueue<>(Comparator.comparing((Order o) -> !o.sameDay()).thenComparingLong(Order::seq));
    }

    /** Runs minute by minute; arrivals are added at their minute; returns the minute each order was picked. */
    public static Map<String, Integer> run(Queue<Order> queue, List<Order> arrivals, int minutes, int reservedForStandard) {
        Map<String, Integer> picked = new HashMap<>();
        for (int minute = 0; minute < minutes; minute++) {
            for (Order o : arrivals) {
                if (o.arrivedMinute() == minute) {
                    queue.add(o);
                }
            }
            int slots = PER_MINUTE;
            if (reservedForStandard > 0) {
                List<Order> oldestStandard = new ArrayList<>(queue.stream().filter(o -> !o.sameDay())
                        .sorted(Comparator.comparingLong(Order::seq)).limit(reservedForStandard).toList());
                for (Order o : oldestStandard) {
                    queue.remove(o);
                    picked.put(o.id(), minute);
                    slots--;
                }
            }
            for (int i = 0; i < slots && !queue.isEmpty(); i++) {
                picked.put(queue.poll().id(), minute);
            }
        }
        return picked;
    }

    private Picking() {
    }
}
