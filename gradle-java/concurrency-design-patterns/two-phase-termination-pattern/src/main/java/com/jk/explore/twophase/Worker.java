package com.jk.explore.twophase;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Takes orders and writes each as three lines. Stopping it takes two phases: first it is asked to stop, and it finishes what it is
 * doing, tidies up and ends; then the caller waits for that, for a limited time.
 */
public class Worker {

    private final BlockingQueue<String> orders = new LinkedBlockingQueue<>();
    private final Ledger ledger;
    private final Thread thread;
    private final AtomicBoolean stopRequested = new AtomicBoolean();
    private final AtomicBoolean cleanedUp = new AtomicBoolean();
    private final AtomicInteger finishedOrders = new AtomicInteger();
    private volatile Runnable beforeSecondLine = () -> { };
    private final boolean checksTheFlag;

    public Worker(Ledger ledger, boolean checksTheFlag) {
        this.ledger = ledger;
        this.checksTheFlag = checksTheFlag;
        this.thread = new Thread(this::run, "worker");
    }

    public void start() {
        thread.start();
    }

    public void submit(String order) {
        orders.add(order);
    }

    /** A hook, called in the middle of every order, between its first and second line. */
    public void beforeSecondLine(Runnable hook) {
        this.beforeSecondLine = hook;
    }

    private void run() {
        try {
            while (!(checksTheFlag && stopRequested.get())) {
                String order = orders.take();
                ledger.begin();
                ledger.writeLine(order + " line 1");
                beforeSecondLine.run();
                ledger.writeLine(order + " line 2");
                ledger.writeLine(order + " line 3");
                ledger.end();
                finishedOrders.incrementAndGet();
            }
        } catch (InterruptedException e) {
            // asked to stop while waiting for an order: fall through to the cleanup
        } catch (IllegalStateException e) {
            // the ledger was closed underneath it
        } finally {
            cleanedUp.set(true);
        }
    }

    /** Phase one: ask it to stop. It will finish the order it is on. */
    public void requestStop(boolean alsoWake) {
        stopRequested.set(true);
        if (alsoWake) {
            thread.interrupt();
        }
    }

    /** Phase two: wait for it to end, for a limited time. Returns whether it did. */
    public boolean awaitStop(long millis) throws InterruptedException {
        thread.join(millis);
        return !thread.isAlive();
    }

    public boolean isAlive() {
        return thread.isAlive();
    }

    public Thread.State state() {
        return thread.getState();
    }

    public boolean cleanedUp() {
        return cleanedUp.get();
    }

    public int finishedOrders() {
        return finishedOrders.get();
    }

    public int pending() {
        return orders.size();
    }
}
