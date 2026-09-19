package com.jk.explore.twophase;

import java.util.List;
import java.util.concurrent.CountDownLatch;

public class TwoPhaseDemo {

    static void until(java.util.function.BooleanSupplier c) {
        long deadline = System.nanoTime() + 10_000_000_000L;
        while (!c.getAsBoolean() && System.nanoTime() < deadline) {
            Thread.onSpinWait();
        }
    }

    /** Starts a worker with one order in progress, held between its first and second line. */
    static Worker holdMidOrder(Ledger ledger, Gate gate, boolean checksTheFlag) throws InterruptedException {
        Worker w = new Worker(ledger, checksTheFlag);
        CountDownLatch inside = new CountDownLatch(1);
        w.beforeSecondLine(() -> {
            inside.countDown();
            gate.await();
        });
        w.start();
        w.submit("ORD-1");
        inside.await();
        return w;
    }

    public static void main(String[] args) throws Exception {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() throws Exception {
        System.out.println("ONE. Pull the plug.");
        Ledger ledger = new Ledger();
        Gate gate = new Gate();
        Worker w = holdMidOrder(ledger, gate, false);
        ledger.close();
        gate.open();
        w.awaitStop(5000);
        System.out.println("  the shop shuts down and closes the ledger while ORD-1 is half written. lines written: " + ledger.lines() + ".");
        System.out.println("  left with an order half written: " + ledger.leftHalfWritten() + ". the order has a line 1 and no line 2 or 3.");
    }

    private static void two() throws Exception {
        System.out.println("TWO. Ask it to stop, and let it finish.");
        Ledger ledger = new Ledger();
        Gate gate = new Gate();
        Worker w = holdMidOrder(ledger, gate, true);
        w.submit("ORD-2");
        w.requestStop(false);
        System.out.println("  stop requested while ORD-1 is half written, and ORD-2 is waiting.");
        gate.open();
        boolean ended = w.awaitStop(5000);
        System.out.println("  the worker ended: " + ended + ". orders finished: " + w.finishedOrders() + ". lines: " + ledger.lines().size() + ", all of ORD-1's, none of ORD-2's.");
        ledger.close();
        System.out.println("  left with an order half written: " + ledger.leftHalfWritten() + ".");
    }

    private static void three() throws Exception {
        System.out.println("THREE. A worker that is asleep.");
        Ledger ledger = new Ledger();
        Worker asleep = new Worker(ledger, true);
        asleep.start();
        until(() -> asleep.state() == Thread.State.WAITING);
        asleep.requestStop(false);
        System.out.println("  a stop request that only sets a flag, to a worker waiting for an order: " + asleep.awaitStop(200) + ", still " + asleep.state() + ".");
        asleep.requestStop(true);
        System.out.println("  the same request, with an interrupt to wake it: " + asleep.awaitStop(5000) + ".");
    }

    private static void four() throws Exception {
        System.out.println("FOUR. Tidy up on the way out.");
        Ledger ledger = new Ledger();
        Worker w = new Worker(ledger, true);
        w.start();
        until(() -> w.state() == Thread.State.WAITING);
        w.requestStop(true);
        w.awaitStop(5000);
        System.out.println("  the worker was interrupted while waiting. did its cleanup run: " + w.cleanedUp() + ".");
        System.out.println("  the cleanup is in a finally block, so it runs however the worker ends.");
    }

    private static void five() throws Exception {
        System.out.println("FIVE. A worker that will not stop.");
        Ledger ledger = new Ledger();
        Gate stuck = new Gate();
        Worker w = holdMidOrder(ledger, stuck, true);
        w.requestStop(true);
        boolean ended = w.awaitStop(200);
        System.out.println("  the worker is stuck in something that ignores the request. after waiting 200 ms: ended " + ended + ", alive " + w.isAlive() + ".");
        System.out.println("  phase two has a time limit. what happens next is a decision: report it, wait longer, or restart the process. Java gives no safe way to force a thread to stop.");
        stuck.open();
        w.awaitStop(5000);
    }

    private static void six() throws Exception {
        System.out.println("SIX. The bill.");
        Ledger ledger = new Ledger();
        Gate gate = new Gate();
        Worker w = holdMidOrder(ledger, gate, true);
        for (int i = 2; i <= 6; i++) {
            w.submit("ORD-" + i);
        }
        w.requestStop(false);
        gate.open();
        w.awaitStop(5000);
        System.out.println("  stopped with 5 orders still waiting: finished " + w.finishedOrders() + ", pending " + w.pending() + ".");
        System.out.println("  those " + w.pending() + " orders were accepted from customers and have not been done. a stop needs a policy: finish them first, hand them to another worker, or save them.");
        System.out.println("  and shutting down took as long as the order in progress. stopping is never instant.");
    }
}
