package com.jk.explore.doublechecked;

import java.io.IOException;
import java.lang.reflect.Modifier;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Supplier;

public class DoubleCheckedDemo {

    /** Two threads ask for the price list at the same moment, having both seen that it does not exist. Returns how many were built. */
    static int race(Supplier<PriceList> get, Runnable reset) throws InterruptedException {
        reset.run();
        PriceList.BUILT.set(0);
        Rendezvous.expect(2);
        try {
            Thread a = new Thread(get::get);
            Thread b = new Thread(get::get);
            a.start();
            b.start();
            a.join();
            b.join();
        } finally {
            Rendezvous.clear();
        }
        return PriceList.BUILT.get();
    }

    public static void main(String[] args) throws Exception {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() throws InterruptedException {
        System.out.println("ONE. Check, then create.");
        System.out.println("  two threads ask for the shared price list at the same moment, before it exists.");
        System.out.println("  price lists built: " + race(NaiveLazy::get, NaiveLazy::reset) + ". both saw that it was missing, and both built one.");
        System.out.println("  each thread now holds a different price list, and one of them is thrown away.");
    }

    private static void two() throws InterruptedException {
        System.out.println("TWO. Lock every time.");
        System.out.println("  the same two threads, with the lock on every call: built " + race(SynchronisedLazy::get, SynchronisedLazy::reset) + ".");
        SynchronisedLazy.reset();
        for (int i = 0; i < 1000; i++) {
            SynchronisedLazy.get();
        }
        System.out.println("  1000 more calls, long after it was built, took the lock " + SynchronisedLazy.LOCKS_TAKEN.get() + " times.");
    }

    private static void three() throws InterruptedException {
        System.out.println("THREE. Check, lock, check again.");
        System.out.println("  the same race: built " + race(DoubleCheckedLazy::get, DoubleCheckedLazy::reset) + ". the second thread waited for the lock, looked again, and found it built.");
        DoubleCheckedLazy.reset();
        for (int i = 0; i < 1000; i++) {
            DoubleCheckedLazy.get();
        }
        System.out.println("  1000 calls: the lock was taken " + DoubleCheckedLazy.LOCKS_TAKEN.get() + " time. after that, no call waits for anyone.");
    }

    private static void four() throws Exception {
        System.out.println("FOUR. Why it must be volatile.");
        boolean isVolatile = Modifier.isVolatile(DoubleCheckedLazy.class.getDeclaredField("instance").getModifiers());
        System.out.println("  the field is declared volatile: " + isVolatile + ".");
        System.out.println("  without it, the Java memory model lets one thread see the reference before it sees the object built.");
        System.out.println("  that failure cannot be produced on demand. it depends on the processor and the compiler. so the rule is guarded by a test, not by a demonstration.");
    }

    private static void five() {
        System.out.println("FIVE. The simplest correct way.");
        PriceList.BUILT.set(0);
        System.out.println("  price lists built before anyone asks: " + PriceList.BUILT.get() + ".");
        PriceList first = HolderLazy.get();
        PriceList second = HolderLazy.get();
        System.out.println("  after two calls: " + PriceList.BUILT.get() + " built, the same one both times: " + (first == second) + ".");
        System.out.println("  the JVM builds a class's static state once, when it is first used. there is no lock and no volatile to write, or to get wrong.");
    }

    private static void six() throws IOException {
        System.out.println("SIX. The bill.");
        int dcl = codeLines("DoubleCheckedLazy.java");
        int holder = codeLines("HolderLazy.java");
        System.out.println("  lines of code in the accessor's class: double-checked " + dcl + ", holder " + holder + ".");
        System.out.println("  double-checked locking is ceremony with one way to be subtly wrong. it earns its place only where the holder idiom cannot be used, for example when creation needs an argument.");
        System.out.println("  and an uncontended lock is cheap. measure before deciding the lock on every call is a problem.");
    }

    private static int codeLines(String file) throws IOException {
        List<String> lines = Files.readAllLines(Path.of("src/main/java/com/jk/explore/doublechecked/" + file));
        int n = 0;
        boolean inComment = false;
        for (String line : lines) {
            String t = line.trim();
            if (t.startsWith("/**") || t.startsWith("/*")) {
                inComment = !t.contains("*/");
                continue;
            }
            if (inComment) {
                inComment = !t.contains("*/");
                continue;
            }
            if (t.isEmpty() || t.startsWith("//") || t.startsWith("import") || t.startsWith("package")) {
                continue;
            }
            n++;
        }
        return n;
    }
}
