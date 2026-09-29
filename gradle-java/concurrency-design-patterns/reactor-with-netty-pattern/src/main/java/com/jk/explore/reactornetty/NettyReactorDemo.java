package com.jk.explore.reactornetty;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;

/**
 * The five acts, with a real Netty server and real TCP connections from 100 tills.
 */
public final class NettyReactorDemo {

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();

        try (ShopServer server = new ShopServer(1, false)) {
            List<Till> tills = connect(server, 100);

            out.add("ONE. One Netty event loop serves every till.");
            out.add("  100 tills connect; till 1 asks \"stock KETTLE-1\": " + tills.get(0).ask("stock KETTLE-1"));
            out.add("  threads running handlers: " + server.handlerThreads());

            out.add("");
            out.add("TWO. The pipeline turns bytes into whole questions.");
            tills.get(1).send("price MU");
            tills.get(1).send("G-1\n");
            out.add("  till 2 sends \"price MU\" and \"G-1\" as two separate writes: answer " + tills.get(1).readLine());
            out.add("  LineBasedFrameDecoder waited for the end of the line; the handler only ever sees whole lines");

            out.add("");
            out.add("THREE. Every till asks at once.");
            List<CompletableFuture<String>> answers = new ArrayList<>();
            for (Till t : tills) {
                answers.add(CompletableFuture.supplyAsync(() -> ask(t, "stock MUG-1")));
            }
            long correct = answers.stream().map(CompletableFuture::join).filter("25"::equals).count();
            out.add("  100 tills ask at once: " + correct + " correct answers; threads running handlers: " + server.handlerThreads());
            close(tills);
        }

        out.add("");
        out.add("FOUR. Several event loops: Netty's multi-reactor.");
        try (ShopServer server = new ShopServer(4, false)) {
            List<Till> tills = connect(server, 100);
            for (Till t : tills) {
                t.ask("stock KETTLE-1");
            }
            out.add("  4 worker event loops: the 100 connections are spread over " + server.eventLoopsServingConnections()
                    + " threads, and each connection always stays on its own");
            close(tills);
        }

        out.add("");
        out.add("FIVE. The bill: a handler that blocks holds up its whole event loop.");
        try (ShopServer server = new ShopServer(1, false)) {
            List<Till> tills = connect(server, 3);
            out.addAll(slowQuestion(tills));
            close(tills);
        }
        try (ShopServer server = new ShopServer(1, true)) {
            List<Till> tills = connect(server, 3);
            out.add("  with the handler on its own executor group: " + slowQuestion(tills).get(1).substring(2));
            close(tills);
        }
        return out;
    }

    private static List<Till> connect(ShopServer server, int n) throws Exception {
        List<Till> tills = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            tills.add(new Till(server.port()));
        }
        return tills;
    }

    private static void close(List<Till> tills) throws Exception {
        for (Till t : tills) {
            t.close();
        }
    }

    private static String ask(Till t, String question) {
        try {
            return t.ask(question);
        } catch (Exception e) {
            return "error";
        }
    }

    /** Till 2 starts a 300 ms report; till 3 then asks a quick question. How long did till 3 wait? */
    private static List<String> slowQuestion(List<Till> tills) throws Exception {
        CompletableFuture<String> report = CompletableFuture.supplyAsync(() -> ask(tills.get(1), "report"));
        Thread.sleep(50);   // let the report start first
        long start = System.nanoTime();
        String answer = tills.get(2).ask("stock KETTLE-1");
        long millis = (System.nanoTime() - start) / 1_000_000;
        report.join();
        List<String> out = new ArrayList<>();
        out.add("  till 3 asks a quick question while till 2's 300 ms report runs: answer " + answer);
        out.add("  " + (millis > 200 ? "it waited over 0.2 s for a question that takes microseconds"
                : "answered in under 0.2 s"));
        return out;
    }

    private NettyReactorDemo() {
    }
}
