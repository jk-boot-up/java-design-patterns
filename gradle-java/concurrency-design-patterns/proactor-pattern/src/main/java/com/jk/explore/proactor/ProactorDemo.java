package com.jk.explore.proactor;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * The five acts: asking suppliers one by one, starting every request at once, completion handlers, a failure as a completion, and the bill.
 */
public final class ProactorDemo {

    static final int[] PRICES = {2100, 1950, 2240, 1890, 2010};

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        List<Supplier> suppliers = new ArrayList<>();
        List<Integer> ports = new ArrayList<>();
        for (int p : PRICES) {
            Supplier s = new Supplier(p);
            suppliers.add(s);
            ports.add(s.port());
        }
        try {
            out.add("ONE. Ask five suppliers for a kettle price, one after another.");
            long t0 = System.nanoTime();
            Map<Integer, Integer> blocking = BlockingQuotes.ask(ports);
            long blockingMs = (System.nanoTime() - t0) / 1_000_000;
            out.add("  " + blocking.size() + " prices in " + (blockingMs >= 900 ? "over 0.9 s" : blockingMs + " ms")
                    + ": each supplier takes 0.2 s, and we waited for each in turn");
            out.add("  the asking thread did nothing else the whole time");

            out.add("");
            out.add("TWO. A proactor: start all five, and be told when each finishes.");
            ProactorQuotes quotes = new ProactorQuotes(ports.size());
            long t1 = System.nanoTime();
            quotes.start(ports);
            out.add("  all 5 requests started, and start() returned, in " + (quotes.startedInMs() < 100 ? "under 0.1 s" : quotes.startedInMs() + " ms"));
            quotes.await(5000);
            long asyncMs = (System.nanoTime() - t1) / 1_000_000;
            out.add("  all 5 answers in " + (asyncMs < 600 ? "under 0.6 s" : asyncMs + " ms") + ": the waits overlapped");

            out.add("");
            out.add("THREE. Completion handlers receive the results.");
            int best = Integer.MAX_VALUE;
            for (int i = 0; i < ports.size(); i++) {
                String r = quotes.results().get(ports.get(i));
                out.add("  supplier " + (i + 1) + ": " + pounds(Integer.parseInt(r)));
                best = Math.min(best, Integer.parseInt(r));
            }
            out.add("  cheapest: " + pounds(best));

            out.add("");
            out.add("FOUR. A failure arrives as a completion too.");
            List<Integer> withDead = new ArrayList<>(ports.subList(0, 2));
            int dead = Supplier.deadPort();
            withDead.add(dead);
            ProactorQuotes q2 = new ProactorQuotes(withDead.size());
            q2.start(withDead);
            q2.await(5000);
            long answered = q2.results().values().stream().filter(v -> !v.startsWith("failed")).count();
            out.add("  supplier 6 is down: its failed() handler ran: " + q2.results().get(dead).startsWith("failed"));
            out.add("  the other " + answered + " answered as normal");

            out.add("");
            out.add("FIVE. The bill: one request, three callbacks.");
            out.add("  connect -> Connected.completed -> write -> Written.completed -> read -> Read.completed");
            out.add("  the steps of one request no longer read top to bottom in one method");
        } finally {
            for (Supplier s : suppliers) {
                s.close();
            }
        }
        return out;
    }

    static String pounds(long pence) {
        return String.format("£%d.%02d", pence / 100, pence % 100);
    }

    private ProactorDemo() {
    }
}
