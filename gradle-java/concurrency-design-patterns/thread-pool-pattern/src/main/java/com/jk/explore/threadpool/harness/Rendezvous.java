package com.jk.explore.threadpool.harness;

import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

/**
 * <strong>Harness piece two: the interleaving forcer.</strong> Named parties
 * meet here and are released together, so a race that "happens sometimes"
 * on the real scheduler is turned into a race that happens on every single
 * run.
 *
 * <p>Every lost-update demonstration in this category has the same shape:
 * two threads each read a shared value, meet at a rendezvous, and then both
 * write back a value derived from the stale read. Without the rendezvous,
 * the two threads might interleave that way, or might not — a test built on
 * that hope is a test that flakes. With it, both threads are provably at
 * the same instant before either writes, every time.
 *
 * <p>This is deliberately a two-or-more-party barrier rather than a general
 * combinatorial "try every interleaving" engine. Every race this category
 * demonstrates — a lost update, a torn read, two locks taken in opposite
 * orders — is forced by pinning threads at one shared point, not by
 * replaying an exhaustive schedule, and a simpler mechanism that is
 * provably correct beats a general one that is harder to trust.
 */
public final class Rendezvous {

    private final CyclicBarrier barrier;
    private final String name;

    public Rendezvous(String name, int parties) {
        this.name = name;
        this.barrier = new CyclicBarrier(parties);
    }

    /** Blocks until every party has called this for the current round. */
    public void meet() {
        try {
            barrier.await(10, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(name + ": interrupted at the rendezvous", e);
        } catch (BrokenBarrierException | TimeoutException e) {
            throw new IllegalStateException(name + ": a party never arrived", e);
        }
    }
}
