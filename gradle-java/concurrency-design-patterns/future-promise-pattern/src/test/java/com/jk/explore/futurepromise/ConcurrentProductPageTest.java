package com.jk.explore.futurepromise;

import com.jk.explore.futurepromise.domain.ProductPageView;
import com.jk.explore.futurepromise.harness.Gate;
import com.jk.explore.futurepromise.pattern.ConcurrentProductPage;
import org.junit.jupiter.api.RepeatedTest;

import java.math.BigDecimal;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ConcurrentProductPageTest {

    @RepeatedTest(20)
    void allThreeLookupsAreInFlightBeforeAnyOneOfThemReturns() throws Exception {
        Gate priceHold = new Gate();
        Gate stockHold = new Gate();
        Gate ratingHold = new Gate();
        CountDownLatch allStarted = new CountDownLatch(3);

        ExecutorService pool = Executors.newFixedThreadPool(3);
        try {
            ConcurrentProductPage page = new ConcurrentProductPage(
                    sku -> { allStarted.countDown(); priceHold.awaitOpen(); return new BigDecimal("9.99"); },
                    sku -> { allStarted.countDown(); stockHold.awaitOpen(); return 3; },
                    sku -> { allStarted.countDown(); ratingHold.awaitOpen(); return 4.0; },
                    pool);

            Thread renderer = new Thread(() -> {
                try {
                    ProductPageView view = page.render("ESP-001");
                    assertEquals(new BigDecimal("9.99"), view.price());
                    assertEquals(3, view.stock());
                    assertEquals(4.0, view.rating());
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }
            });
            renderer.start();

            // All three lookups are provably running at once -- not merely
            // submitted -- before any of them is released.
            assertTrue(allStarted.await(2, TimeUnit.SECONDS),
                    "all three lookups must start concurrently, not one at a time");

            priceHold.open();
            stockHold.open();
            ratingHold.open();
            renderer.join(2_000);
        } finally {
            pool.shutdown();
            pool.awaitTermination(2, TimeUnit.SECONDS);
        }
    }
}
