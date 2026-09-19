package com.jk.explore.readwritelock;

import com.jk.explore.readwritelock.domain.Price;
import com.jk.explore.readwritelock.harness.Gate;
import com.jk.explore.readwritelock.pattern.ReadWriteCatalogue;
import org.junit.jupiter.api.RepeatedTest;

import java.math.BigDecimal;
import java.util.concurrent.CountDownLatch;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ReadWriteCatalogueTest {

    private static final Price ORIGINAL = new Price(new BigDecimal("49.99"), "GBP");

    @RepeatedTest(20)
    void severalReadersHoldTheReadLockAtTheSameMomentProvenNotGuessed() throws InterruptedException {
        ReadWriteCatalogue catalogue = new ReadWriteCatalogue(ORIGINAL);
        int readerCount = 4;
        Gate readersHold = new Gate();
        CountDownLatch allHoldingTheLock = new CountDownLatch(readerCount);

        Thread[] readers = new Thread[readerCount];
        for (int i = 0; i < readerCount; i++) {
            readers[i] = new Thread(() -> {
                catalogue.lock().readLock().lock();
                try {
                    allHoldingTheLock.countDown();
                    readersHold.awaitOpen();
                } finally {
                    catalogue.lock().readLock().unlock();
                }
            });
            readers[i].start();
        }

        // Every reader is confirmed to be holding the read lock, at once,
        // before this asserts on the lock's own reported count.
        allHoldingTheLock.await();
        assertEquals(readerCount, catalogue.lock().getReadLockCount(),
                "all four readers must be able to hold the read lock at the same time");

        readersHold.open();
        for (Thread reader : readers) {
            reader.join(2_000);
        }
        assertEquals(0, catalogue.lock().getReadLockCount());
    }
}
