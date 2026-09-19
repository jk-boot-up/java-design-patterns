package com.jk.explore.futurepromise.naive;

import com.jk.explore.futurepromise.domain.Lookup;
import com.jk.explore.futurepromise.domain.ProductPageView;

import java.math.BigDecimal;

/**
 * <strong>The naive version.</strong> Three lookups, called one after the
 * other, each waited out fully before the next begins — even though none
 * of the three depends on either of the other two. The page pays for all
 * three delays, added together, for no reason the data itself demands.
 */
public final class SequentialProductPage {

    private final Lookup<BigDecimal> price;
    private final Lookup<Integer> stock;
    private final Lookup<Double> rating;

    public SequentialProductPage(Lookup<BigDecimal> price, Lookup<Integer> stock, Lookup<Double> rating) {
        this.price = price;
        this.stock = stock;
        this.rating = rating;
    }

    public ProductPageView render(String sku) {
        long start = System.nanoTime();
        BigDecimal p = price.fetch(sku);
        int s = stock.fetch(sku);
        double r = rating.fetch(sku);
        return new ProductPageView(p, s, r, System.nanoTime() - start);
    }
}
