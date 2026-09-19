package com.jk.explore.producerconsumer;

import com.jk.explore.producerconsumer.domain.Order;
import com.jk.explore.producerconsumer.harness.Gate;
import com.jk.explore.producerconsumer.pattern.BoundedOrderQueue;
import com.jk.explore.producerconsumer.pattern.Packer;
import org.junit.jupiter.api.RepeatedTest;

import java.util.concurrent.CountDownLatch;

import static org.junit.jupiter.api.Assertions.assertEquals;

class PackerTest {

    @RepeatedTest(20)
    void poisonDrainsEverythingQueuedBeforeIt() throws InterruptedException {
        BoundedOrderQueue queue = new BoundedOrderQueue(10);
        Packer packer = new Packer(queue, order -> { });
        Thread thread = new Thread(packer);
        thread.start();

        for (int i = 1; i <= 4; i++) {
            queue.put(new Order("ord-" + i, "BNS-220"));
        }
        queue.put(Packer.POISON);
        thread.join(2_000);

        assertEquals(4, packer.packed().size(),
                "every order queued before the poison pill must be packed");
    }

    /**
     * The known race for an abrupt shutdown: one order is held mid-pack, a
     * fixed number more are queued behind it, and the packer thread is
     * interrupted rather than sent a poison pill. Forced with a rendezvous
     * latch rather than hoped for with timing, so this fails every run if
     * it is ever going to fail at all.
     */
    @RepeatedTest(20)
    void interruptingThePackerLosesWhateverIsStillQueued() throws InterruptedException {
        BoundedOrderQueue queue = new BoundedOrderQueue(10);
        Gate hold = new Gate();
        CountDownLatch started = new CountDownLatch(1);
        Packer packer = new Packer(queue, order -> {
            started.countDown();
            try {
                hold.awaitOpen();
            } catch (IllegalStateException e) {
                // the gate converts our interrupt into this; that is expected here.
            }
        });
        Thread thread = new Thread(packer);
        thread.start();

        queue.put(new Order("ord-holding", "BNS-220"));
        started.await();
        for (int i = 1; i <= 3; i++) {
            queue.put(new Order("ord-" + i, "BNS-220"));
        }

        thread.interrupt();
        thread.join(2_000);

        assertEquals(3, queue.size(), "the three orders behind the held one must still be queued");
        assertEquals(0, packer.packed().size(), "nothing behind the held order was ever packed");
    }
}
