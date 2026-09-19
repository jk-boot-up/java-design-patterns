package com.jk.explore.producerconsumer;

import com.jk.explore.producerconsumer.domain.Order;
import com.jk.explore.producerconsumer.harness.Gate;
import com.jk.explore.producerconsumer.naive.ThreadPerOrderCheckout;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ThreadPerOrderCheckoutTest {

    @Test
    void everyCheckoutGetsItsOwnLiveThread() throws InterruptedException {
        Gate hold = new Gate();
        ThreadPerOrderCheckout checkout = new ThreadPerOrderCheckout(order -> hold.awaitOpen());

        checkout.checkout(new Order("ord-1", "BNS-220"));
        checkout.checkout(new Order("ord-2", "BNS-220"));
        checkout.checkout(new Order("ord-3", "BNS-220"));

        long giveUpAt = System.currentTimeMillis() + 2_000;
        while (checkout.liveThreads() < 3 && System.currentTimeMillis() < giveUpAt) {
            Thread.onSpinWait();
        }
        assertEquals(3, checkout.liveThreads(),
                "three checkouts must produce three live threads, all still parked on packing");

        hold.open();
    }

    @Test
    void floodSafelyNeverExceedsTheRequestedCount() {
        Gate hold = new Gate();
        ThreadPerOrderCheckout.FloodResult result = ThreadPerOrderCheckout.floodSafely(50, hold);

        assertEquals(50, result.threadsCreated());
        assertTrue(result.avgCreateMicros() >= 0);
    }
}
