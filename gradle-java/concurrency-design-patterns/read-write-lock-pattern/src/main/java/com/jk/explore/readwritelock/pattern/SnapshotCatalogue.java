package com.jk.explore.readwritelock.pattern;

import com.jk.explore.readwritelock.domain.Price;

import java.util.concurrent.atomic.AtomicReference;

/**
 * <strong>The honest alternative a read-write lock is often measured
 * against and loses to.</strong> {@link Price} is immutable, so publishing
 * a new one is a single atomic reference swap — no lock needed at all,
 * because a reader either sees the whole old price or the whole new one,
 * never a mixture. For a critical section this short, the lock's own
 * bookkeeping — acquiring, releasing, tracking which readers hold it —
 * can cost more than the work it protects.
 */
public final class SnapshotCatalogue {

    private final AtomicReference<Price> price;

    public SnapshotCatalogue(Price initial) {
        this.price = new AtomicReference<>(initial);
    }

    public Price read() {
        return price.get();
    }

    public void write(Price newPrice) {
        price.set(newPrice);
    }
}
