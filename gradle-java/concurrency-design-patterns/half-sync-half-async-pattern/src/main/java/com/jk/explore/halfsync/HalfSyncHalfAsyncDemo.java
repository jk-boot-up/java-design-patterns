package com.jk.explore.halfsync;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: blocking work on the event thread, an async half that only queues, a sync half of plain workers, a queue that absorbs a burst, and the bill.
 */
public final class HalfSyncHalfAsyncDemo {

    static final int BURST = 20;

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();

        out.add("ONE. The event thread does every order's blocking work itself.");
        EventThreadOnly old = new EventThreadOnly();
        old.burst(BURST);
        out.add("  " + BURST + " orders arrive at once; each needs 100 ms to save, charge and email");
        out.add("  the last order waited " + (old.worstAcceptMs() >= 1500 ? "over 1.5 s" : old.worstAcceptMs() + " ms")
                + " just to be accepted");

        out.add("");
        out.add("TWO. The async half only accepts, and queues.");
        HalfSyncHalfAsync hsha = new HalfSyncHalfAsync(4, 100);
        hsha.startWorkers();
        long t0 = System.nanoTime();
        hsha.burst(BURST);
        out.add("  every order accepted within " + (hsha.worstAcceptMs() < 100 ? "0.1 s" : hsha.worstAcceptMs() + " ms")
                + "; the event thread is free again at once");

        out.add("");
        out.add("THREE. The sync half: plain workers running plain code.");
        hsha.awaitDone(BURST, 10_000);
        long allMs = (System.nanoTime() - t0) / 1_000_000;
        out.add("  4 worker threads each take an order and run save, charge, email, in order");
        out.add("  all " + hsha.done() + " orders done in " + (allMs < 1000 ? "under 1 s" : allMs + " ms"));
        hsha.stop();

        out.add("");
        out.add("FOUR. The queue in the middle absorbs the burst.");
        out.add("  at the busiest moment the queue held " + (hsha.peakQueue() >= 10 ? "10 or more" : hsha.peakQueue())
                + " orders waiting for a worker");
        out.add("  the event thread never waited for a card payment; only the workers did");

        out.add("");
        out.add("FIVE. The bill: a full queue must say no.");
        HalfSyncHalfAsync stuck = new HalfSyncHalfAsync(4, 10);
        stuck.burst(BURST);
        out.add("  workers stalled (the card provider is down), queue of 10: " + stuck.turnedAway()
                + " of " + BURST + " orders turned away");
        out.add("  every queue needs a limit, and a plan for what happens beyond it");
        return out;
    }

    private HalfSyncHalfAsyncDemo() {
    }
}
