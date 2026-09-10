package com.jk.explore.iterator;

import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;

/**
 * The page loop, written once.
 *
 * <p>This is the pattern's whole idea. Everything awkward about the feed --
 * page numbers, when to fetch the next page, how you know you have finished --
 * lives in this one class, and nowhere else in the project. A caller sees
 * products, one after another, and never learns that pages exist.
 *
 * <p>Two things are worth noticing, because they are what a hand-written loop
 * does not give you for free.
 *
 * <p><b>It remembers where you are.</b> The position is a field here, not in
 * the catalogue. So the catalogue can hand out two iterators at once and they
 * do not tread on each other -- which is what makes a nested loop over the
 * same catalogue work.
 *
 * <p><b>It is lazy.</b> A page is fetched the first time somebody asks for a
 * product on it. Stop halfway through the catalogue and the pages you never
 * reached are never requested.
 *
 * <p>The class is package-private on purpose: callers get it from {@link
 * ProductCatalogue#iterator()} and only ever use it through the {@link
 * Iterator} interface, so its name is not part of the public shape.
 */
class CatalogueIterator implements Iterator<Product> {

    private final CatalogueFeed feed;

    /** The page we are currently handing products out of. */
    private List<Product> currentPage = List.of();

    /** Which page {@link #currentPage} is, and where we are inside it. */
    private int pageNumber = 0;
    private int indexInPage = 0;

    /** False until the first page has actually been fetched. */
    private boolean started = false;

    CatalogueIterator(CatalogueFeed feed) {
        this.feed = feed;
    }

    /**
     * True while there is another product to hand out.
     *
     * <p>This is where the fetching happens. If we have run off the end of the
     * page we are on, we ask for the next one; an empty page means the
     * catalogue is finished.
     */
    @Override
    public boolean hasNext() {
        if (!started) {
            currentPage = feed.page(pageNumber);
            started = true;
        }
        while (indexInPage >= currentPage.size()) {
            if (currentPage.isEmpty()) {
                return false;
            }
            pageNumber++;
            indexInPage = 0;
            currentPage = feed.page(pageNumber);
        }
        return true;
    }

    /** The next product. Always ask {@link #hasNext()} first. */
    @Override
    public Product next() {
        if (!hasNext()) {
            throw new NoSuchElementException("the catalogue has no more products");
        }
        return currentPage.get(indexInPage++);
    }
}
