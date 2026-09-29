package com.jk.explore.backpressure;

import java.util.concurrent.Flow;

/**
 * The pattern with Java's own Reactive Streams interfaces: the publisher sends only as many items as the subscriber has asked for.
 */
public final class PullPublisher implements Flow.Publisher<Integer> {

    private final int total;
    private int maxOutstanding;

    public PullPublisher(int total) {
        this.total = total;
    }

    @Override
    public void subscribe(Flow.Subscriber<? super Integer> subscriber) {
        subscriber.onSubscribe(new Flow.Subscription() {
            private int next = 1;
            private long requested;
            private boolean emitting;

            public void request(long n) {
                requested += n;
                maxOutstanding = (int) Math.max(maxOutstanding, requested);
                if (emitting) {
                    return;
                }
                emitting = true;
                while (requested > 0 && next <= total) {
                    requested--;
                    subscriber.onNext(next++);
                }
                emitting = false;
                if (next > total) {
                    subscriber.onComplete();
                }
            }

            public void cancel() {
                next = total + 1;
            }
        });
    }

    /** The most items the subscriber ever had outstanding at once. */
    public int maxOutstanding() {
        return maxOutstanding;
    }
}
