package com.jk.explore.producerconsumer;

import com.jk.explore.producerconsumer.domain.Order;
import com.jk.explore.producerconsumer.domain.Packing;
import com.jk.explore.producerconsumer.harness.Gate;
import com.jk.explore.producerconsumer.naive.InlineCheckout;
import com.jk.explore.producerconsumer.naive.ThreadPerOrderCheckout;
import com.jk.explore.producerconsumer.pattern.BoundedOrderQueue;
import com.jk.explore.producerconsumer.pattern.Packer;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

/**
 * Five acts. The only deliberate delay anywhere in this class is
 * {@link #PACK_MILLIS} — packing genuinely does take longer than an order
 * arrives, and that gap is the entire subject of this project, so it is
 * named and printed rather than hidden.
 */
public final class PackingWarehouseDemo {

    /** How long packing one order takes. The named, measured subject of this whole demo. */
    private static final long PACK_MILLIS = 40;

    private static final Packing REAL_PACKING = order -> {
        try {
            Thread.sleep(PACK_MILLIS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    };

    public static void main(String[] args) throws InterruptedException {
        System.out.println("PRODUCER-CONSUMER — orders arrive faster than they are packed\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
    }

    private static void actOne() {
        System.out.println("ONE. No queue at all — checkout packs the order itself.");
        InlineCheckout checkout = new InlineCheckout(REAL_PACKING);
        long totalNanos = 0;
        for (int i = 1; i <= 3; i++) {
            long took = checkout.checkout(new Order("ord-" + i, "BNS-220"));
            totalNanos += took;
            System.out.printf("  checkout(ord-%d) returned after %.0fms%n", i, took / 1_000_000.0);
        }
        System.out.printf("  three checkouts, %.0fms of it spent packing, on the checkout thread%n",
                totalNanos / 1_000_000.0);
        System.out.println("  every customer behind order one waited for order one's pack.");
        System.out.println();
    }

    private static void actTwo() throws InterruptedException {
        System.out.println("TWO. A thread per order — works, until it does not.");
        Gate hold = new Gate();
        int sample = 2_000;
        ThreadPerOrderCheckout.FloodResult result = ThreadPerOrderCheckout.floodSafely(sample, hold);
        System.out.printf("  created %,d real threads in %.1fms (%.1f microseconds each)%n",
                result.threadsCreated(), result.totalCreateNanos() / 1_000_000.0,
                result.avgCreateMicros());
        double perThousandMs = (result.avgCreateMicros() * 1000) / 1000.0;
        System.out.printf("  at that rate, 100,000 threads costs roughly %.0fms of creation",
                result.avgCreateMicros() * 100_000 / 1000.0);
        System.out.println(" alone —");
        System.out.println("  before any of them has packed a single order.");
        System.out.println("  each thread also holds a stack (default ~512KB-1MB);");
        System.out.println("  that is where OutOfMemoryError: unable to create native");
        System.out.println("  thread comes from. Not simulated here — a laptop that");
        System.out.println("  actually hits that limit is not a teaching aid.");
        System.out.println();
    }

    private static void actThree() throws InterruptedException {
        System.out.println("THREE. The bounded queue — and what 'full' costs.");
        int capacity = 3;
        BoundedOrderQueue queue = new BoundedOrderQueue(capacity);
        Gate packerHold = new Gate();
        CountDownLatch started = new CountDownLatch(1);
        Packer packer = new Packer(queue, order -> {
            started.countDown();
            packerHold.awaitOpen();
        });
        Thread packerThread = new Thread(packer, "packer");
        packerThread.start();

        // Put one order, and wait until the packer has actually taken it and
        // is parked mid-pack, so it cannot race the next puts for a slot.
        // Only then fill the remaining capacity — "full" is forced, not hoped for.
        queue.put(new Order("ord-holding", "BNS-220"));
        started.await();
        for (int i = 1; i <= capacity; i++) {
            queue.put(new Order("ord-" + i, "BNS-220"));
        }
        System.out.println("  queue filled to capacity " + capacity + ": " + queue.size());

        boolean accepted = queue.offer(new Order("ord-overflow", "BNS-220"), 150, TimeUnit.MILLISECONDS);
        System.out.println("  one more order, offered with a 150ms patience: "
                + (accepted ? "accepted" : "REJECTED — the queue never had room in time"));

        packerHold.open();
        // The gate is now permanently open, so every remaining pack() call
        // returns immediately and the packer drains the queue on its own.
        // Once it has, tell it to stop -- otherwise it is left parked in
        // take() forever, a live thread the JVM will wait on at exit.
        while (queue.size() > 0) {
            Thread.onSpinWait();
        }
        queue.put(Packer.POISON);
        packerThread.join(2_000);
        System.out.println("  released: the packer drains the " + capacity + " that were queued");
        System.out.println();
    }

    private static void actFour() throws InterruptedException {
        System.out.println("FOUR. Clean shutdown — the queue drains before the packer stops.");
        BoundedOrderQueue queue = new BoundedOrderQueue(10);
        Packer packer = new Packer(queue, REAL_PACKING);
        Thread packerThread = new Thread(packer, "packer");
        packerThread.start();

        for (int i = 1; i <= 4; i++) {
            queue.put(new Order("ord-" + i, "BNS-220"));
        }
        queue.put(Packer.POISON);
        packerThread.join(5_000);

        System.out.println("  4 orders queued, then the poison pill.");
        System.out.println("  packed before stopping: " + packer.packed().size() + " of 4");
        System.out.println();
    }

    private static void actFive() throws InterruptedException {
        System.out.println("FIVE. Abrupt shutdown — whatever is still queued is lost.");
        BoundedOrderQueue queue = new BoundedOrderQueue(10);
        Gate packerHold = new Gate();
        CountDownLatch startedPacking = new CountDownLatch(1);
        Thread packerThread = new Thread(() -> {
            try {
                queue.take();                 // takes ord-holding
                startedPacking.countDown();
                packerHold.awaitOpen();        // parked here — never returns in this act
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } catch (IllegalStateException e) {
                // Gate.awaitOpen() converts the interrupt above into this;
                // for this demo that is the same "stop now" signal.
            }
        }, "packer");
        packerThread.start();

        queue.put(new Order("ord-holding", "BNS-220"));
        startedPacking.await();
        for (int i = 1; i <= 4; i++) {
            queue.put(new Order("ord-" + i, "BNS-220"));
        }

        packerThread.interrupt();
        packerThread.join(2_000);

        System.out.println("  1 order was being packed, 4 more were queued behind it.");
        System.out.println("  the packer thread was interrupted, not signalled to drain.");
        System.out.println("  orders lost, still in the queue: " + queue.size());
    }
}
