package com.jk.explore.backpressurereactor;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.atomic.AtomicReference;
import org.reactivestreams.Subscription;
import reactor.core.publisher.BaseSubscriber;
import reactor.core.publisher.Flux;
import reactor.core.publisher.FluxSink;
import reactor.core.scheduler.Schedulers;

/**
 * The five acts, with Project Reactor: a supplier's product feed into a slow search indexer.
 */
public final class ReactorBackpressureDemo {

    static final int PRODUCTS = 10_000;

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();

        out.add("ONE. A feed that pushes regardless of demand.");
        AtomicReference<Throwable> failure = new AtomicReference<>();
        AtomicInteger indexed = new AtomicInteger();
        CountDownLatch done = new CountDownLatch(1);
        Flux.<Integer>create(sink -> {
                    for (int i = 1; i <= PRODUCTS; i++) {
                        sink.next(i);            // ignores how much the indexer asked for
                    }
                    sink.complete();
                }, FluxSink.OverflowStrategy.IGNORE)
                .publishOn(Schedulers.single(), 256)
                .subscribe(p -> {
                    slowIndex();
                    indexed.incrementAndGet();
                }, e -> {
                    failure.set(e);
                    done.countDown();
                }, done::countDown);
        done.await(30, TimeUnit.SECONDS);
        out.add("  the indexer's queue holds 256; Reactor stops the stream: "
                + (failure.get() == null ? "no error" : failure.get().getClass().getSimpleName()));
        out.add("  indexed before it failed: " + (indexed.get() < PRODUCTS ? "only part" : "all") + " of the " + PRODUCTS
                + " products; the rest were refused, not quietly piled up");

        out.add("");
        out.add("TWO. A feed that produces only what is asked for.");
        AtomicLong maxOutstanding = new AtomicLong();
        AtomicLong outstanding = new AtomicLong();
        AtomicInteger got = new AtomicInteger();
        Flux.range(1, PRODUCTS)
                .doOnRequest(n -> maxOutstanding.accumulateAndGet(outstanding.addAndGet(n), Math::max))
                .doOnNext(p -> outstanding.decrementAndGet())
                .subscribe(new BaseSubscriber<Integer>() {
                    @Override
                    protected void hookOnSubscribe(Subscription s) {
                        request(10);
                    }

                    @Override
                    protected void hookOnNext(Integer p) {
                        if (got.incrementAndGet() % 10 == 0) {
                            request(10);
                        }
                    }
                });
        out.add("  the indexer requests 10 at a time: indexed " + got.get() + ", never more than "
                + maxOutstanding.get() + " asked for and not yet delivered");

        out.add("");
        out.add("THREE. limitRate(10): Reactor does the asking.");
        List<Long> requests = new ArrayList<>();
        AtomicInteger count = new AtomicInteger();
        Flux.range(1, 100)
                .doOnRequest(requests::add)
                .limitRate(10)
                .subscribe(p -> count.incrementAndGet());
        out.add("  the feed saw requests of " + requests.subList(0, 4) + " ... for " + count.get() + " products");
        out.add("  it asks for 10, then tops up by 8 each time three-quarters is used, so the pipe never runs dry");

        out.add("");
        out.add("FOUR. Stock levels: only the latest matters.");
        List<Integer> delivered = new ArrayList<>();
        AtomicReference<BaseSubscriber<Integer>> indexer = new AtomicReference<>();
        Flux.<Integer>create(sink -> {
                    for (int level = 1000; level >= 1; level--) {
                        sink.next(level);
                    }
                    sink.complete();
                })
                .onBackpressureLatest()
                .subscribe(new BaseSubscriber<Integer>() {
                    @Override
                    protected void hookOnSubscribe(Subscription s) {
                        indexer.set(this);
                        request(1);
                    }

                    @Override
                    protected void hookOnNext(Integer level) {
                        delivered.add(level);
                    }
                });
        indexer.get().request(1);
        out.add("  1000 stock-level updates for one mug; the shop asked twice and got " + delivered);
        out.add("  onBackpressureLatest kept only the newest while nobody was asking");

        out.add("");
        out.add("FIVE. The bill: every source must choose.");
        out.add("  a source that can wait is simplest: range, generate, a database cursor");
        out.add("  one that cannot must buffer (memory), drop, or keep the latest (data lost); Reactor makes you say which");
        out.add("  and an unbounded onBackpressureBuffer() just moves the pile somewhere harder to see");
        return out;
    }

    private static void slowIndex() {
        try {
            Thread.sleep(1);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private ReactorBackpressureDemo() {
    }
}
