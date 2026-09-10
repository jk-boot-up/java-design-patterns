package com.jk.explore.iterator;

import java.util.Iterator;

/**
 * The shop's catalogue, as the rest of the code would like it to be: a thing
 * you can loop over.
 *
 * <p>The class is four lines of real code, and that is the point. It wraps the
 * paged {@link CatalogueFeed} and implements {@link Iterable}, so Java's
 * for-each loop works on it:
 *
 * <pre>{@code
 * for (Product product : catalogue) {
 *     System.out.println(product);
 * }
 * }</pre>
 *
 * <p>There is no magic in that loop. When the compiler sees for-each over an
 * {@code Iterable}, it calls {@link #iterator()} once and then calls {@code
 * hasNext()} and {@code next()} until it is told to stop. Implementing the
 * interface is what buys you the syntax -- and, for free, everything else in
 * the JDK that takes an {@code Iterable}.
 *
 * <p>Note what this class does <em>not</em> hold: there is no current page and
 * no current position on it. Position belongs to the iterator, so every call
 * to {@link #iterator()} starts a fresh, independent walk.
 */
public class ProductCatalogue implements Iterable<Product> {

    private final CatalogueFeed feed;

    public ProductCatalogue(CatalogueFeed feed) {
        this.feed = feed;
    }

    /** A fresh walk over the catalogue, starting at the first product. */
    @Override
    public Iterator<Product> iterator() {
        return new CatalogueIterator(feed);
    }
}
