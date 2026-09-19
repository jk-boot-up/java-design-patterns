package com.jk.explore.activeobject.pattern;

import com.jk.explore.activeobject.harness.Gate;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

/**
 * <strong>The costs of the pattern, measured.</strong> Two of the three
 * costs need a real number rather than a claim: how far the mailbox backs
 * up, and how many messages one worker can get through.
 */
public final class Mailbox {

    private Mailbox() {
    }

    /**
     * Parks the worker on a gate, sends {@code messages} more, and reports
     * how many are waiting. Nothing is dropped and nothing pushes back.
     */
    public static int backlogWhileWorkerIsBusy(int messages) throws InterruptedException {
        try (InventoryActiveObject inventory = new InventoryActiveObject(0)) {
            Gate slow = new Gate();
            CountDownLatch started = new CountDownLatch(1);
            CompletableFuture<Integer> first = inventory.importCorrection(0, () -> {
                started.countDown();
                slow.awaitOpen();
            });
            started.await();
            List<CompletableFuture<Integer>> pending = new ArrayList<>();
            for (int i = 0; i < messages; i++) {
                pending.add(inventory.restock(1));
            }
            int backlog = inventory.pendingMessages();
            slow.open();
            first.join();
            pending.get(pending.size() - 1).join();
            return backlog;
        }
    }

    public record Throughput(int callers, int messages, long millis, long perSecond) {
    }

    /** Several caller threads send as fast as they can; each message costs {@code workNanos} of real work, all of it on one worker. */
    public static Throughput throughput(int callers, int messagesPerCaller, long workNanos) throws InterruptedException {
        try (InventoryActiveObject inventory = new InventoryActiveObject(0)) {
            Gate start = new Gate();
            CompletableFuture<?>[] lasts = new CompletableFuture<?>[callers];
            Thread[] threads = new Thread[callers];
            for (int c = 0; c < callers; c++) {
                int index = c;
                threads[c] = new Thread(() -> {
                    start.awaitOpen();
                    CompletableFuture<Integer> last = null;
                    for (int i = 0; i < messagesPerCaller; i++) {
                        last = inventory.restockWithWork(1, workNanos);
                    }
                    lasts[index] = last;
                });
                threads[c].start();
            }
            long began = System.nanoTime();
            start.open();
            for (Thread t : threads) {
                t.join();
            }
            CompletableFuture.allOf(lasts).orTimeout(30, TimeUnit.SECONDS).join();
            long nanos = Math.max(1, System.nanoTime() - began);
            int total = callers * messagesPerCaller;
            return new Throughput(callers, total, nanos / 1_000_000, total * 1_000_000_000L / nanos);
        }
    }
}
