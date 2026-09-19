package com.jk.explore.readwritelock;

import com.jk.explore.readwritelock.domain.Price;
import com.jk.explore.readwritelock.pattern.SnapshotCatalogue;
import org.junit.jupiter.api.RepeatedTest;

import java.math.BigDecimal;
import java.util.concurrent.CountDownLatch;

import static org.junit.jupiter.api.Assertions.assertTrue;

class SnapshotCatalogueTest {

    private static final Price ORIGINAL = new Price(new BigDecimal("49.99"), "GBP");
    private static final Price UPDATED = new Price(new BigDecimal("54.99"), "EUR");

    @RepeatedTest(20)
    void aReaderNeverSeesATornPriceEvenWithNoLockAtAll() throws InterruptedException {
        SnapshotCatalogue catalogue = new SnapshotCatalogue(ORIGINAL);
        CountDownLatch stop = new CountDownLatch(1);
        boolean[] sawTornPrice = {false};

        Thread reader = new Thread(() -> {
            while (stop.getCount() > 0) {
                Price p = catalogue.read();
                if (!p.equals(ORIGINAL) && !p.equals(UPDATED)) {
                    sawTornPrice[0] = true;
                }
            }
        });
        reader.start();

        for (int i = 0; i < 5_000; i++) {
            catalogue.write(i % 2 == 0 ? UPDATED : ORIGINAL);
        }
        stop.countDown();
        reader.join(2_000);

        assertTrue(!sawTornPrice[0],
                "an immutable Price published through an AtomicReference is always read whole");
    }
}
