package com.jk.explore.backpressure;

import java.util.concurrent.Flow;

/**
 * The search indexer as a subscriber: asks for a batch, indexes it, then asks for the next.
 */
public final class Indexer implements Flow.Subscriber<Integer> {

    private final int batch;
    private Flow.Subscription subscription;
    private int indexed;
    private int inBatch;
    private boolean done;

    public Indexer(int batch) {
        this.batch = batch;
    }

    public void onSubscribe(Flow.Subscription s) {
        subscription = s;
        s.request(batch);
    }

    public void onNext(Integer product) {
        indexed++;
        if (++inBatch == batch) {
            inBatch = 0;
            subscription.request(batch);
        }
    }

    public void onError(Throwable t) {
        done = true;
    }

    public void onComplete() {
        done = true;
    }

    public int indexed() {
        return indexed;
    }

    public boolean done() {
        return done;
    }
}
