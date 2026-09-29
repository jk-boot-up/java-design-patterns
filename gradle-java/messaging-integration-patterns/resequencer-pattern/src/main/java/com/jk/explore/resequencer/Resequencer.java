package com.jk.explore.resequencer;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.function.Consumer;

/**
 * The pattern: holds messages that arrive early, and releases each order's messages strictly in sequence.
 *
 * <p>Each order has its own next-expected number and its own buffer. A message
 * with the expected number is released, followed by any buffered ones that now
 * follow on. A gap that never fills can be skipped after {@code maxHeld}
 * messages are waiting behind it.
 */
public final class Resequencer {

    private final Consumer<StatusUpdate> next;
    private final int maxHeld;
    private final Map<String, Integer> expected = new HashMap<>();
    private final Map<String, TreeMap<Integer, StatusUpdate>> held = new HashMap<>();
    private final List<String> trace = new ArrayList<>();

    public Resequencer(Consumer<StatusUpdate> next, int maxHeld) {
        this.next = next;
        this.maxHeld = maxHeld;
    }

    public void accept(StatusUpdate u) {
        TreeMap<Integer, StatusUpdate> buffer = held.computeIfAbsent(u.orderId(), k -> new TreeMap<>());
        buffer.put(u.seq(), u);
        release(u.orderId(), buffer);
        if (!buffer.isEmpty()) {
            trace.add("received " + u + "; holding " + buffer.keySet());
        }
        if (buffer.size() >= maxHeld) {
            int skipTo = buffer.firstKey();
            trace.add("gap before #" + skipTo + " never filled: skipping ahead");
            expected.put(u.orderId(), skipTo);
            release(u.orderId(), buffer);
        }
    }

    private void release(String orderId, TreeMap<Integer, StatusUpdate> buffer) {
        int want = expected.getOrDefault(orderId, 1);
        while (buffer.containsKey(want)) {
            StatusUpdate out = buffer.remove(want);
            trace.add("released " + out);
            next.accept(out);
            want++;
        }
        expected.put(orderId, want);
    }

    public List<String> trace() {
        return trace;
    }

    public int holding(String orderId) {
        return held.getOrDefault(orderId, new TreeMap<>()).size();
    }
}
