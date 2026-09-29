package com.jk.explore.cas;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.BooleanSupplier;

/**
 * A flash sale: many buyer threads, each trying to buy several kettles at once.
 */
public final class FlashSale {

    public static int run(int threads, int triesEach, BooleanSupplier buy) throws InterruptedException {
        AtomicInteger sold = new AtomicInteger();
        List<Thread> buyers = new ArrayList<>();
        for (int t = 0; t < threads; t++) {
            buyers.add(new Thread(() -> {
                for (int i = 0; i < triesEach; i++) {
                    if (buy.getAsBoolean()) {
                        sold.incrementAndGet();
                    }
                }
            }));
        }
        buyers.forEach(Thread::start);
        for (Thread b : buyers) {
            b.join();
        }
        return sold.get();
    }

    private FlashSale() {
    }
}
