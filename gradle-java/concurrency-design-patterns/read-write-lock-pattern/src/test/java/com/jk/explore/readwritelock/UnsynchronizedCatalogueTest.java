package com.jk.explore.readwritelock;

import com.jk.explore.readwritelock.domain.Price;
import com.jk.explore.readwritelock.harness.Gate;
import com.jk.explore.readwritelock.naive.UnsynchronizedCatalogue;
import org.junit.jupiter.api.RepeatedTest;

import java.math.BigDecimal;
import java.util.concurrent.CountDownLatch;

import static org.junit.jupiter.api.Assertions.assertEquals;

class UnsynchronizedCatalogueTest {

    private static final Price ORIGINAL = new Price(new BigDecimal("49.99"), "GBP");
    private static final Price UPDATED = new Price(new BigDecimal("54.99"), "EUR");

    @RepeatedTest(20)
    void aReadInTheGapSeesTheNewAmountWithTheOldCurrencyEveryRun() throws InterruptedException {
        Gate midWrite = new Gate();
        CountDownLatch amountSet = new CountDownLatch(1);
        UnsynchronizedCatalogue catalogue = new UnsynchronizedCatalogue(ORIGINAL, () -> {
            amountSet.countDown();
            midWrite.awaitOpen();
        });

        Thread writer = new Thread(() -> catalogue.write(UPDATED));
        writer.start();

        // The new amount is set before this latch can fire, and the writer
        // cannot set the new currency until the gate below opens -- so this
        // read is proven to land in the gap between the two field writes.
        amountSet.await();
        Price torn = catalogue.read();
        midWrite.open();
        writer.join(2_000);

        assertEquals(UPDATED.amount(), torn.amount(), "the new amount must already be visible");
        assertEquals(ORIGINAL.currency(), torn.currency(), "the currency must not have changed yet");
    }
}
