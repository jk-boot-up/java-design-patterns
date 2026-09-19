package com.jk.explore.activeobject.pattern;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.function.IntUnaryOperator;

/**
 * <strong>The active object: its own thread, its own mailbox, no lock.</strong>
 *
 * <p>A capstone made of parts met earlier: the queue from §46, a thread
 * from §47, a future from §48, and state owned by one party from §50.
 * The {@code stock} field is plain. It is read and written only by the
 * worker thread, so there is nothing to lock.
 */
public class InventoryActiveObject implements AutoCloseable {

    private final BlockingQueue<Runnable> mailbox = new LinkedBlockingQueue<>();
    private final Thread worker;
    private int stock; // touched only by the worker thread
    private volatile boolean running = true;

    public InventoryActiveObject(int initial) {
        this.stock = initial;
        this.worker = new Thread(this::runMessages, "inventory-worker");
        this.worker.setDaemon(true);
        this.worker.start();
    }

    /** Returns at once. The future completes with the new stock once the worker has done it. */
    public CompletableFuture<Integer> reserve(int amount) {
        return send(current -> current - amount);
    }

    public CompletableFuture<Integer> restock(int amount) {
        return send(current -> current + amount);
    }

    /** A slow import: {@code slowWork} runs on the worker, ahead of every message behind it. */
    public CompletableFuture<Integer> importCorrection(int correctStock, Runnable slowWork) {
        return send(current -> {
            slowWork.run();
            return correctStock;
        });
    }

    /** A message that fails <em>on the worker</em>, to show where the failure surfaces. */
    public CompletableFuture<Integer> failWith(String reason) {
        return send(current -> {
            throw new IllegalStateException(reason + " [raised on " + Thread.currentThread().getName() + "]");
        });
    }

    /** A restock that does {@code spinNanos} of real work first, so the worker is the bottleneck. */
    public CompletableFuture<Integer> restockWithWork(int amount, long spinNanos) {
        return send(current -> {
            long until = System.nanoTime() + spinNanos;
            while (System.nanoTime() < until) {
                Thread.onSpinWait();
            }
            return current + amount;
        });
    }

    public CompletableFuture<Integer> available() {
        return send(current -> current);
    }

    /** How many messages are waiting in the mailbox, not yet started. */
    public int pendingMessages() {
        return mailbox.size();
    }

    public String workerName() {
        return worker.getName();
    }

    private CompletableFuture<Integer> send(IntUnaryOperator change) {
        CompletableFuture<Integer> reply = new CompletableFuture<>();
        mailbox.add(() -> {
            try {
                stock = change.applyAsInt(stock);
                reply.complete(stock);
            } catch (RuntimeException e) {
                reply.completeExceptionally(e);
            }
        });
        return reply;
    }

    private void runMessages() {
        while (running) {
            try {
                mailbox.take().run();
            } catch (InterruptedException e) {
                return;
            }
        }
    }

    @Override
    public void close() {
        running = false;
        worker.interrupt();
    }
}
