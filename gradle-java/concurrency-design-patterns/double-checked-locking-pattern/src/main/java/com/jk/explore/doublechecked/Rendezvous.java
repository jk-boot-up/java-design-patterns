package com.jk.explore.doublechecked;

import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;

/**
 * A test hook: when set, threads meet here right after they have seen that the price list does not exist yet.
 * It makes the unlucky interleaving happen every time, instead of once in a million.
 */
public final class Rendezvous {

    private static volatile CyclicBarrier barrier;

    private Rendezvous() {
    }

    public static void expect(int threads) {
        barrier = new CyclicBarrier(threads);
    }

    public static void clear() {
        barrier = null;
    }

    static void meet() {
        CyclicBarrier b = barrier;
        if (b != null) {
            try {
                b.await();
            } catch (InterruptedException | BrokenBarrierException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}
