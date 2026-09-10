package com.jk.explore.iterator;

import java.util.ArrayList;
import java.util.List;

/**
 * Browsing the catalogue without the pattern: every caller writes the page
 * loop out by hand.
 *
 * <p>This class is the "before" picture. It works, and for one method it is
 * perfectly readable. The trouble starts when a second method needs to walk
 * the catalogue too, because the page loop has to be written again -- and the
 * copy is where the bugs live. Both are real mistakes, kept here deliberately
 * so the tests can show them.
 *
 * <p><b>Bug one:</b> {@link #countProducts()} advances the page number inside
 * the {@code if}, so it never moves past page 0 when a page is full, and
 * loops forever. It is written here as a bounded loop instead, which is the
 * shape people reach for once they have been bitten -- and it stops early.
 *
 * <p><b>Bug two:</b> {@link #findCheapest()} starts at page 1 rather than page
 * 0, so it silently misses the first three products. Nothing throws. The shop
 * just quietly stops showing its cheapest item.
 */
public class NaiveCatalogueBrowser {

    private final CatalogueFeed feed;

    public NaiveCatalogueBrowser(CatalogueFeed feed) {
        this.feed = feed;
    }

    /** Correct: the page loop, written carefully. */
    public List<Product> allProducts() {
        List<Product> found = new ArrayList<>();
        int pageNumber = 0;
        while (true) {
            List<Product> page = feed.page(pageNumber);
            if (page.isEmpty()) {
                break;
            }
            found.addAll(page);
            pageNumber++;
        }
        return found;
    }

    /**
     * The same loop again, capped at three pages "to be safe". On a catalogue
     * with more than nine products the count is simply wrong, and no one finds
     * out until a customer complains.
     */
    public int countProducts() {
        int count = 0;
        for (int pageNumber = 0; pageNumber < 3; pageNumber++) {
            count += feed.page(pageNumber).size();
        }
        return count;
    }

    /**
     * The same loop a third time, with an off-by-one start. Page 0 is never
     * fetched, so the first three products are invisible to this method.
     */
    public Product findCheapest() {
        Product cheapest = null;
        int pageNumber = 1;
        while (true) {
            List<Product> page = feed.page(pageNumber);
            if (page.isEmpty()) {
                break;
            }
            for (Product product : page) {
                if (cheapest == null || product.priceInPounds() < cheapest.priceInPounds()) {
                    cheapest = product;
                }
            }
            pageNumber++;
        }
        return cheapest;
    }
}
