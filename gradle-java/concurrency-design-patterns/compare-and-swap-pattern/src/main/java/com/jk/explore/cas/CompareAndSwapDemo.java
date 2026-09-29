package com.jk.explore.cas;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * The five acts: check-then-act, a lock, a compare-and-swap loop, the loop in one call, and the bill.
 */
public final class CompareAndSwapDemo {

    static final int KETTLES = 100;
    static final int BUYERS = 8;
    static final int TRIES = 50;

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        out.add("Flash sale: " + KETTLES + " kettles, " + BUYERS + " buyer threads, each trying " + TRIES + " times.");
        out.add("");

        out.add("ONE. Check, then act, with no protection.");
        UnsafeStock unsafe = new UnsafeStock(KETTLES);
        int sold1 = FlashSale.run(BUYERS, TRIES, unsafe::buyOne);
        out.add("  kettles sold: " + (sold1 > KETTLES ? "more than " + KETTLES : sold1) + ", from a stock of " + KETTLES);
        out.add("  two buyers saw the same count, and both took the same kettle: oversold");

        out.add("");
        out.add("TWO. A lock: one buyer at a time.");
        LockedStock locked = new LockedStock(KETTLES);
        int sold2 = FlashSale.run(BUYERS, TRIES, locked::buyOne);
        out.add("  kettles sold: " + sold2 + "; left: " + locked.left());
        out.add("  correct, but every other buyer waits in line while one checks");

        out.add("");
        out.add("THREE. Compare-and-swap: take it only if nobody else did.");
        CasStock cas = new CasStock(KETTLES);
        int sold3 = FlashSale.run(BUYERS, TRIES, cas::buyOne);
        out.add("  kettles sold: " + sold3 + "; left: " + cas.left());
        out.add("  no locks; a buyer who lost the race just looked again (" + (cas.retries() > 0 ? "it happened" : "not this time") + ")");

        out.add("");
        out.add("FOUR. The loop in one call.");
        CasStock shortWay = new CasStock(KETTLES);
        int sold4 = FlashSale.run(BUYERS, TRIES, shortWay::buyOneShort);
        out.add("  getAndUpdate(s -> s > 0 ? s - 1 : s): sold " + sold4 + ", left " + shortWay.left());

        out.add("");
        out.add("FIVE. The bill: one value at a time.");
        AtomicInteger stock = new AtomicInteger(KETTLES);
        AtomicInteger buyersRecorded = new AtomicInteger();
        stock.decrementAndGet();
        out.add("  a buyer takes a kettle, then its thread stops before recording who bought it");
        out.add("  stock " + stock.get() + ", buyers recorded " + buyersRecorded.get() + ": two atomic values, not one atomic change");
        out.add("  and under heavy contention, threads spin retrying instead of waiting");
        return out;
    }

    private CompareAndSwapDemo() {
    }
}
