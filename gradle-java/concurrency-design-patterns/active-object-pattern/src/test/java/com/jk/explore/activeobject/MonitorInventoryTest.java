package com.jk.explore.activeobject;

import com.jk.explore.activeobject.harness.Gate;
import com.jk.explore.activeobject.naive.MonitorInventory;
import org.junit.jupiter.api.RepeatedTest;

import java.util.concurrent.CountDownLatch;

import static org.junit.jupiter.api.Assertions.assertEquals;

class MonitorInventoryTest {

    @RepeatedTest(20)
    void aCheckoutCallerIsBlockedBehindASlowImport() throws InterruptedException {
        MonitorInventory inventory = new MonitorInventory(10);
        Gate slow = new Gate();
        CountDownLatch inside = new CountDownLatch(1);
        Thread importer = new Thread(() -> inventory.importCorrection(50, () -> {
            inside.countDown();
            slow.awaitOpen();
        }));
        importer.start();
        inside.await();

        Thread checkout = new Thread(() -> inventory.reserve(1));
        checkout.start();
        while (checkout.getState() != Thread.State.WAITING) {
            Thread.onSpinWait();
        }
        assertEquals(Thread.State.WAITING, checkout.getState());

        slow.open();
        importer.join(5_000);
        checkout.join(5_000);
        assertEquals(49, inventory.available());
    }
}
