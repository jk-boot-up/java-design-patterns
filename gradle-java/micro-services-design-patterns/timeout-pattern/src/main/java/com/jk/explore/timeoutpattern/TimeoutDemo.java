package com.jk.explore.timeoutpattern;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class TimeoutDemo {

    public static void main(String[] args) throws Exception {
        ExecutorService pool = Executors.newCachedThreadPool();
        try {
            one(pool);
            two(pool);
            three(pool);
            four();
            five();
            six();
        } finally {
            pool.shutdownNow();
        }
    }

    private static void one(ExecutorService pool) throws Exception {
        System.out.println("ONE. No timeout.");
        Gate gate = new Gate();
        SupplierApi api = new SupplierApi(gate);
        Thread page = new Thread(() -> api.stockOf("MUG-BLUE"), "product-page");
        page.start();
        long until = System.nanoTime() + 5_000_000_000L;
        while (page.getState() != Thread.State.WAITING && System.nanoTime() < until) {
            Thread.onSpinWait();
        }
        System.out.println("  the supplier never answers. the product page's thread is: " + page.getState() + ", with no limit on for how long.");
        System.out.println("  nothing in the code says it will ever come back, and the customer is looking at a spinner.");
        gate.open();
        page.join();
    }

    private static void two(ExecutorService pool) {
        System.out.println("TWO. A limit on the wait.");
        SupplierApi api = new SupplierApi(new Gate());
        String shown = new Callers(pool).withTimeout(api, "MUG-BLUE", 100);
        System.out.println("  the same call, with a limit of 100 milliseconds: the page shows \"" + shown + "\".");
        System.out.println("  the page loaded, without the number it could not get.");
    }

    private static void three(ExecutorService pool) throws Exception {
        System.out.println("THREE. Giving up does not stop the work.");
        Gate gate = new Gate();
        SupplierApi api = new SupplierApi(gate);
        new Callers(pool).withTimeout(api, "MUG-BLUE", 100);
        System.out.println("  the caller gave up. calls started at the supplier: " + api.started() + ", finished: " + api.finished() + ".");
        gate.open();
        long deadline = System.nanoTime() + 5_000_000_000L;
        while (api.finished() < 1 && System.nanoTime() < deadline) {
            Thread.onSpinWait();
        }
        System.out.println("  later the supplier finishes anyway: finished " + api.finished() + ". nobody was waiting for the answer, and the work was done.");
    }

    private static void four() {
        System.out.println("FOUR. Choosing the number.");
        List<Integer> day = Latency.aTypicalHundred();
        for (int limit : new int[]{50, 100, 250, 1000, 3000}) {
            System.out.println("  a limit of " + String.format("%4d", limit) + " ms: " + Latency.succeedingWithin(day, limit) + " of 100 calls succeed.");
        }
        System.out.println("  too tight and healthy calls fail. too loose and a slow supplier holds a thread for seconds.");
    }

    private static void five() {
        System.out.println("FIVE. One budget for the whole page.");
        int[] wanted = {400, 700, 500};
        int perCallLimit = 1000;
        int worstCase = wanted.length * perCallLimit;
        System.out.println("  a page makes 3 supplier calls in a row, each allowed " + perCallLimit + " ms. the worst case for the page is " + worstCase + " ms.");
        List<Budget.Outcome> outcomes = Budget.spend(1000, wanted);
        StringBuilder log = new StringBuilder();
        for (Budget.Outcome o : outcomes) {
            log.append("call ").append(o.call()).append(": ").append(o.what());
            log.append(o.what().equals("skipped") ? ", no budget left. " : " at " + o.spentMillis() + " ms. ");
        }
        System.out.println("  with one budget of 1000 ms shared by all three: " + log.toString().trim() + " total " + Budget.total(outcomes) + " ms.");
    }

    private static void six() throws Exception {
        System.out.println("SIX. The bill: you do not know what happened.");
        Gate gate = new Gate();
        SupplierApi payments = new SupplierApi(gate);
        ExecutorService pool = Executors.newCachedThreadPool();
        CompletableFuture<String> charge = new Callers(pool).start(payments, "CHARGE-4999");
        try {
            charge.get(100, java.util.concurrent.TimeUnit.MILLISECONDS);
        } catch (java.util.concurrent.TimeoutException e) {
            System.out.println("  the payment call timed out. the customer is told: we could not take your payment.");
        }
        gate.open();
        long deadline = System.nanoTime() + 5_000_000_000L;
        while (payments.finished() < 1 && System.nanoTime() < deadline) {
            Thread.onSpinWait();
        }
        System.out.println("  the payment provider then completed the charge: charges taken " + payments.finished() + ". the customer thinks nothing was taken.");
        System.out.println("  a timeout says only that you stopped waiting. retrying a payment without an idempotency key would charge again.");
        pool.shutdownNow();
    }
}
