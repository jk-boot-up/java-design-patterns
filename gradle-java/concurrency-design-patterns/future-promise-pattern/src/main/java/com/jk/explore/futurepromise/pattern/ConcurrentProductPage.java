package com.jk.explore.futurepromise.pattern;

import com.jk.explore.futurepromise.domain.Lookup;
import com.jk.explore.futurepromise.domain.ProductPageView;

import java.math.BigDecimal;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Future;

/**
 * <strong>The pattern.</strong> Each lookup is submitted and returns a
 * {@link Future} immediately — a handle to a result that does not exist
 * yet. All three run at once, and the page waits for all three together
 * rather than one after the other, so the total cost is roughly the
 * slowest single lookup, not the sum of all three.
 */
public final class ConcurrentProductPage {

    private final Lookup<BigDecimal> price;
    private final Lookup<Integer> stock;
    private final Lookup<Double> rating;
    private final ExecutorService pool;

    public ConcurrentProductPage(Lookup<BigDecimal> price, Lookup<Integer> stock, Lookup<Double> rating,
            ExecutorService pool) {
        this.price = price;
        this.stock = stock;
        this.rating = rating;
        this.pool = pool;
    }

    public ProductPageView render(String sku) throws ExecutionException, InterruptedException {
        long start = System.nanoTime();

        Future<BigDecimal> priceFuture = pool.submit(callable(() -> price.fetch(sku)));
        Future<Integer> stockFuture = pool.submit(callable(() -> stock.fetch(sku)));
        Future<Double> ratingFuture = pool.submit(callable(() -> rating.fetch(sku)));

        // Each future is asked for its value only after all three lookups are
        // already in flight -- this is what makes them concurrent rather than
        // merely deferred.
        BigDecimal p = priceFuture.get();
        int s = stockFuture.get();
        double r = ratingFuture.get();

        return new ProductPageView(p, s, r, System.nanoTime() - start);
    }

    private static <T> Callable<T> callable(java.util.function.Supplier<T> supplier) {
        return supplier::get;
    }
}
