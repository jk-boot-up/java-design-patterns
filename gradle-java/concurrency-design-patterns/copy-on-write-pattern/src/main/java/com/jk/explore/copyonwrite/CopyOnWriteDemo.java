package com.jk.explore.copyonwrite;

import java.util.ArrayList;
import java.util.ConcurrentModificationException;
import java.util.Iterator;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * The five acts: a plain list changed while being read, a copy-on-write list, readers with no locks, snapshots, and the bill.
 */
public final class CopyOnWriteDemo {

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();

        out.add("ONE. A plain list, changed while it is being read.");
        List<PriceListener> plain = new ArrayList<>();
        List<String> heard = new ArrayList<>();
        plain.add((sku, p) -> heard.add("web page cache"));
        plain.add((sku, p) -> {
            heard.add("loyalty service");
            plain.add((s2, p2) -> heard.add("email service"));
        });
        plain.add((sku, p) -> heard.add("phone app"));
        try {
            for (PriceListener l : plain) {
                l.priceChanged("KETTLE-1", 2700);
            }
        } catch (ConcurrentModificationException e) {
            out.add("  kettle price changes; the loyalty service subscribes the email service while being told");
            out.add("  ConcurrentModificationException after: " + heard);
            out.add("  the phone app never heard about the new price");
        }

        out.add("");
        out.add("TWO. A copy-on-write list: the same thing, no failure.");
        CowList<PriceListener> cow = new CowList<>();
        List<String> heard2 = new ArrayList<>();
        cow.add((sku, p) -> heard2.add("web page cache"));
        cow.add((sku, p) -> {
            heard2.add("loyalty service");
            if (heard2.stream().filter("loyalty service"::equals).count() == 1) {
                cow.add((s2, p2) -> heard2.add("email service"));
            }
        });
        cow.add((sku, p) -> heard2.add("phone app"));
        for (PriceListener l : cow) {
            l.priceChanged("KETTLE-1", 2700);
        }
        out.add("  first change reached: " + heard2);
        heard2.clear();
        for (PriceListener l : cow) {
            l.priceChanged("KETTLE-1", 2500);
        }
        out.add("  next change reached:  " + heard2);

        out.add("");
        out.add("THREE. Readers never lock, and are never disturbed.");
        CowList<PriceListener> busy = new CowList<>();
        AtomicInteger calls = new AtomicInteger();
        for (int i = 0; i < 5; i++) {
            busy.add((s, p) -> calls.incrementAndGet());
        }
        AtomicInteger failures = new AtomicInteger();
        Thread writer = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                PriceListener l = (s, p) -> calls.incrementAndGet();
                busy.add(l);
                busy.remove(l);
            }
        });
        writer.start();
        for (int pass = 0; pass < 100_000; pass++) {
            try {
                for (PriceListener l : busy) {
                    l.priceChanged("MUG-1", 800);
                }
            } catch (RuntimeException e) {
                failures.incrementAndGet();
            }
        }
        writer.join();
        out.add("  100,000 notification passes while another thread subscribes and unsubscribes 1,000 times");
        out.add("  failures: " + failures.get() + "; locks taken by readers: 0");

        out.add("");
        out.add("FOUR. Each reader sees a snapshot.");
        CowList<PriceListener> snap = new CowList<>();
        for (int i = 0; i < 3; i++) {
            snap.add((s, p) -> { });
        }
        Iterator<PriceListener> it = snap.iterator();
        snap.add((s, p) -> { });
        int seen = 0;
        while (it.hasNext()) {
            it.next();
            seen++;
        }
        out.add("  a reader started with " + seen + " listeners; the list now has " + snap.size());
        out.add("  the reader finishes with what it started with; the next reader sees the new one");

        out.add("");
        out.add("FIVE. The bill: every write copies everything.");
        CowList<PriceListener> big = new CowList<>();
        for (int i = 0; i < 10_000; i++) {
            big.add((s, p) -> { });
        }
        out.add("  10,000 listeners added one at a time: " + String.format("%,d", big.elementsCopied()) + " references copied");
        out.add("  fine for lists read often and changed rarely; wrong for lists that change all the time");
        return out;
    }

    private CopyOnWriteDemo() {
    }
}
