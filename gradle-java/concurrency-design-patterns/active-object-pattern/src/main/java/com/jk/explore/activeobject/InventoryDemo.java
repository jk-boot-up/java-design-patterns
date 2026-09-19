package com.jk.explore.activeobject;

import com.jk.explore.activeobject.harness.Gate;
import com.jk.explore.activeobject.naive.MonitorInventory;
import com.jk.explore.activeobject.pattern.InventoryActiveObject;
import com.jk.explore.activeobject.pattern.Mailbox;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutionException;

/**
 * Six acts. No act calls {@code Thread.sleep} to wait for another thread.
 * This capstone re-teaches nothing: it links to the four projects its parts
 * came from and shows only what assembling them adds.
 */
public final class InventoryDemo {

    public static void main(String[] args) throws Exception {
        System.out.println("ACTIVE OBJECT — a call that returns before the work does\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    private static void actOne() throws InterruptedException {
        System.out.println("ONE. A monitor — the checkout thread waits on a slow import.");
        MonitorInventory inventory = new MonitorInventory(10);
        Gate slow = new Gate();
        CountDownLatch inside = new CountDownLatch(1);
        Thread importer = new Thread(() -> inventory.importCorrection(50, () -> {
            inside.countDown();
            slow.awaitOpen();
        }), "import");
        importer.start();
        inside.await();

        Thread checkout = new Thread(() -> inventory.reserve(1), "checkout");
        checkout.start();
        while (checkout.getState() != Thread.State.WAITING) {
            Thread.onSpinWait();
        }
        System.out.println("  the import holds the lock. the checkout thread state: " + checkout.getState());
        System.out.println("  a customer is waiting behind a back-office import.\n");
        slow.open();
        importer.join();
        checkout.join();
    }

    private static void actTwo() throws Exception {
        System.out.println("TWO. An active object — the call returns at once.");
        try (InventoryActiveObject inventory = new InventoryActiveObject(10)) {
            Gate slow = new Gate();
            CountDownLatch started = new CountDownLatch(1);
            CompletableFuture<Integer> imported = inventory.importCorrection(50, () -> {
                started.countDown();
                slow.awaitOpen();
            });
            started.await();
            CompletableFuture<Integer> reserved = inventory.reserve(1);
            System.out.println("  the import is running. reserve(1) has already returned.");
            System.out.println("  its result is ready yet: " + reserved.isDone());
            slow.open();
            System.out.println("  import done: stock " + imported.get());
            System.out.println("  reserve done, later, in order: stock " + reserved.get() + "\n");
        }
    }

    private static void actThree() throws Exception {
        System.out.println("THREE. No lock at all — one thread owns the state.");
        try (InventoryActiveObject inventory = new InventoryActiveObject(0)) {
            int callers = 4, each = 25_000;
            Thread[] threads = new Thread[callers];
            for (int c = 0; c < callers; c++) {
                threads[c] = new Thread(() -> {
                    for (int i = 0; i < each; i++) {
                        inventory.restock(1);
                    }
                });
                threads[c].start();
            }
            for (Thread t : threads) {
                t.join();
            }
            System.out.println("  " + callers + " callers x " + each + " restocks: stock "
                    + inventory.available().get());
            System.out.println("  the stock field has no lock and is not volatile.");
            System.out.println("  only the thread named " + inventory.workerName() + " ever touches it.\n");
        }
    }

    private static void actFour() throws InterruptedException {
        System.out.println("FOUR. The mailbox backs up.");
        int backlog = Mailbox.backlogWhileWorkerIsBusy(10_000);
        System.out.println("  worker busy on one slow message; callers sent 10000 more.");
        System.out.println("  messages waiting in the mailbox: " + backlog);
        System.out.println("  nothing refused them and nothing slowed the callers down.\n");
    }

    private static void actFive() throws InterruptedException {
        System.out.println("FIVE. Errors arrive later, from the worker.");
        try (InventoryActiveObject inventory = new InventoryActiveObject(10)) {
            CompletableFuture<Integer> failed = inventory.failWith("stock feed unavailable");
            try {
                failed.get();
            } catch (ExecutionException e) {
                System.out.println("  cause: " + e.getCause().getMessage());
                StackTraceElement top = e.getCause().getStackTrace()[0];
                System.out.println("  the calling method appears nowhere in that trace: "
                        + !containsFrame(e.getCause(), "actFive"));
                System.out.println("  first frame: " + top.getClassName() + "\n");
            }
        }
    }

    private static void actSix() throws InterruptedException {
        System.out.println("SIX. One worker is a ceiling.");
        long work = 50_000; // each message costs 50 microseconds of real work
        Mailbox.Throughput one = Mailbox.throughput(1, 4_000, work);
        Mailbox.Throughput four = Mailbox.throughput(4, 1_000, work);
        System.out.println("  every message costs 50 microseconds of work, done by the one worker.");
        System.out.println("  1 caller:  " + one.messages() + " messages in " + one.millis() + "ms, "
                + one.perSecond() + " per second");
        System.out.println("  4 callers: " + four.messages() + " messages in " + four.millis() + "ms, "
                + four.perSecond() + " per second");
        System.out.println("  four times the callers, the same rate: the ceiling is the worker, not the callers.");
        System.out.println("\n  where this idea went: actors and event loops.");
    }

    private static boolean containsFrame(Throwable t, String method) {
        for (StackTraceElement e : t.getStackTrace()) {
            if (e.getMethodName().contains(method)) {
                return true;
            }
        }
        return false;
    }
}
