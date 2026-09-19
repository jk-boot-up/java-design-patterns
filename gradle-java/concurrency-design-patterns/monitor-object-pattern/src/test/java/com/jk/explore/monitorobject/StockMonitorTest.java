package com.jk.explore.monitorobject;

import com.jk.explore.monitorobject.harness.Gate;
import com.jk.explore.monitorobject.pattern.StockMonitor;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

import java.util.concurrent.CountDownLatch;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class StockMonitorTest {

    @RepeatedTest(20)
    void concurrentSalesNeverLoseAnUpdate() throws InterruptedException {
        int threads = 8, each = 5_000;
        StockMonitor stock = new StockMonitor(threads * each);
        Gate start = new Gate();
        Thread[] all = new Thread[threads];
        for (int i = 0; i < threads; i++) {
            all[i] = new Thread(() -> {
                start.awaitOpen();
                for (int n = 0; n < each; n++) {
                    stock.sellOne();
                }
            });
            all[i].start();
        }
        start.open();
        for (Thread t : all) {
            t.join(10_000);
        }
        assertEquals(0, stock.available());
    }

    @RepeatedTest(20)
    void aThreadWaitingForStockIsReleasedByTheThreadThatAddsIt() throws InterruptedException {
        StockMonitor stock = new StockMonitor(0);
        CountDownLatch done = new CountDownLatch(1);
        Thread taker = new Thread(() -> {
            try {
                stock.take(3);
                done.countDown();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        taker.start();
        stock.add(2);
        assertTrue(!done.await(50, java.util.concurrent.TimeUnit.MILLISECONDS),
                "two items are not enough; the taker must still be waiting");
        stock.add(1);
        assertTrue(done.await(5, java.util.concurrent.TimeUnit.SECONDS));
        assertEquals(0, stock.available());
    }

    @Test
    void aSecondCallerIsBlockedWhileTheMonitorIsBusy() throws InterruptedException {
        StockMonitor stock = new StockMonitor(5);
        Gate release = new Gate();
        CountDownLatch inside = new CountDownLatch(1);
        Thread holder = new Thread(() -> stock.addAndNotify(1, () -> {
            inside.countDown();
            release.awaitOpen();
        }));
        holder.start();
        inside.await();

        Thread second = new Thread(stock::sellOne);
        second.start();
        while (second.getState() != Thread.State.WAITING) {
            Thread.onSpinWait();
        }
        assertEquals(Thread.State.WAITING, second.getState(), "parked on the monitor's lock");

        release.open();
        second.join(5_000);
        holder.join(5_000);
        assertEquals(5, stock.available());
    }
}
