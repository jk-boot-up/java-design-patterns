package com.jk.explore.readwritelock;

import com.jk.explore.readwritelock.domain.Price;
import com.jk.explore.readwritelock.naive.SingleLockCatalogue;
import org.junit.jupiter.api.RepeatedTest;

import java.math.BigDecimal;
import java.util.concurrent.CountDownLatch;

import static org.junit.jupiter.api.Assertions.assertTrue;

class SingleLockCatalogueTest {

    private static final Price ORIGINAL = new Price(new BigDecimal("49.99"), "GBP");
    private static final Price UPDATED = new Price(new BigDecimal("54.99"), "EUR");

    @RepeatedTest(20)
    void aReaderNeverSeesATornPriceUnderConcurrentWrites() throws InterruptedException {
        SingleLockCatalogue catalogue = new SingleLockCatalogue(ORIGINAL);
        CountDownLatch stop = new CountDownLatch(1);
        boolean[] sawTornPrice = {false};

        Thread reader = new Thread(() -> {
            while (stop.getCount() > 0) {
                Price p = catalogue.read();
                boolean matchesOriginal = p.equals(ORIGINAL);
                boolean matchesUpdated = p.equals(UPDATED);
                if (!matchesOriginal && !matchesUpdated) {
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

        assertTrue(!sawTornPrice[0], "the lock must make every read see one whole price, never a mixture");
    }
}
