package com.jk.explore.reactor;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: a thread per connection, one reactor thread, handlers by event, many clients answered, and the bill.
 */
public final class ReactorDemo {

    static final int TILLS = 100;

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    static void waitUntil(java.util.function.BooleanSupplier done) throws InterruptedException {
        for (int i = 0; i < 200 && !done.getAsBoolean(); i++) {
            Thread.sleep(10);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();

        out.add("ONE. A thread for every connection.");
        try (ThreadPerConnection old = new ThreadPerConnection(); Clients tills = new Clients(old.port(), TILLS)) {
            waitUntil(() -> old.threadsStarted() == TILLS);
            out.add("  " + TILLS + " shop tills connect and wait: " + old.threadsStarted() + " threads, almost all of them idle");
            out.add("  till 1 asks \"stock KETTLE-1\": " + tills.ask(0, "stock KETTLE-1"));
        }

        out.add("");
        out.add("TWO. A reactor: one thread waits on every connection at once.");
        try (Reactor reactor = new Reactor(); Clients tills = new Clients(reactor.port(), TILLS)) {
            out.add("  " + TILLS + " tills connect to the reactor");
            out.add("  till 1 asks \"stock KETTLE-1\": " + tills.ask(0, "stock KETTLE-1"));
            out.add("  threads running handlers: " + reactor.handlerThreads());

            out.add("");
            out.add("THREE. Each kind of event has its handler.");
            out.add("  a new connection -> the accept handler registers it for reading");
            out.add("  bytes arrive     -> the read handler answers the line");
            out.add("  till 2 asks \"price MUG-1\": " + tills.ask(1, "price MUG-1"));

            out.add("");
            out.add("FOUR. Every till is answered by the one thread.");
            int correct = 0;
            for (int i = 0; i < TILLS; i++) {
                tills.send(i, "stock MUG-1");
            }
            for (int i = 0; i < TILLS; i++) {
                if ("20".equals(tills.read(i))) {
                    correct++;
                }
            }
            out.add("  " + TILLS + " tills ask at once: " + correct + " correct answers");
            out.add("  threads running handlers: still " + reactor.handlerThreads());

            out.add("");
            out.add("FIVE. The bill: one slow handler holds up everyone.");
            tills.send(2, "report");
            Thread.sleep(50);
            long start = System.nanoTime();
            String quick = tills.ask(3, "stock KETTLE-1");
            long waited = (System.nanoTime() - start) / 1_000_000;
            tills.read(2);
            out.add("  till 3 asks a quick question while till 2's 300 ms report runs: answer " + quick);
            out.add("  it waited " + (waited >= 200 ? "over 200 ms" : waited + " ms") + " for a question that takes microseconds");
            out.add("  handlers must never block; slow work goes to another thread");
        }
        return out;
    }

    private ReactorDemo() {
    }
}
