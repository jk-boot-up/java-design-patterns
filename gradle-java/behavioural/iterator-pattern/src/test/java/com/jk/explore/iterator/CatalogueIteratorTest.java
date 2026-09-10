package com.jk.explore.iterator;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Iterator;
import java.util.NoSuchElementException;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * The two properties that a hand-written page loop does not give you: the
 * iterator is lazy, and it owns its own position.
 */
class CatalogueIteratorTest {

    @Test
    @DisplayName("a page is fetched only when a product on it is reached")
    void fetchingIsLazy() {
        CatalogueFeed feed = CatalogueFeed.sampleShop();
        ProductCatalogue catalogue = new ProductCatalogue(feed);

        Iterator<Product> products = catalogue.iterator();
        assertEquals(0, feed.pagesFetched(), "nothing should be fetched before the first hasNext()");

        products.next();
        products.next();
        assertEquals(1, feed.pagesFetched(), "two products fit on page 0, so only page 0 is needed");

        products.next();
        products.next();
        assertEquals(2, feed.pagesFetched(), "the fourth product is on page 1");
    }

    @Test
    @DisplayName("stopping early leaves the rest of the catalogue unfetched")
    void stoppingEarlyCostsNothing() {
        CatalogueFeed feed = CatalogueFeed.sampleShop();

        int shown = 0;
        for (Product ignored : new ProductCatalogue(feed)) {
            if (++shown == 2) {
                break;
            }
        }

        assertEquals(1, feed.pagesFetched(), "pages 1 and 2 were never reached, so never requested");
    }

    @Test
    @DisplayName("two iterators over one catalogue keep separate positions")
    void positionsAreIndependent() {
        ProductCatalogue catalogue = new ProductCatalogue(CatalogueFeed.sampleShop());

        Iterator<Product> outer = catalogue.iterator();
        Iterator<Product> inner = catalogue.iterator();

        outer.next();
        outer.next();

        assertEquals("SKU-001", inner.next().sku(), "the second iterator was dragged along by the first");
        assertEquals("SKU-003", outer.next().sku());
    }

    @Test
    @DisplayName("hasNext() is false at the end, and next() then throws")
    void endOfCatalogue() {
        Iterator<Product> products = new ProductCatalogue(CatalogueFeed.sampleShop()).iterator();
        for (int i = 0; i < 8; i++) {
            products.next();
        }

        assertFalse(products.hasNext());
        assertThrows(NoSuchElementException.class, products::next);
    }

    @Test
    @DisplayName("an empty catalogue simply has nothing to walk")
    void emptyCatalogue() {
        ProductCatalogue empty = new ProductCatalogue(new CatalogueFeed(java.util.List.of()));

        Iterator<Product> products = empty.iterator();
        assertFalse(products.hasNext());

        int visits = 0;
        for (Product ignored : empty) {
            visits++;
        }
        assertEquals(0, visits, "for-each over an empty catalogue should not run the body");
    }

    @Test
    @DisplayName("hasNext() can be called repeatedly without consuming anything")
    void hasNextDoesNotConsume() {
        Iterator<Product> products = new ProductCatalogue(CatalogueFeed.sampleShop()).iterator();

        assertTrue(products.hasNext());
        assertTrue(products.hasNext());
        assertTrue(products.hasNext());

        assertEquals("SKU-001", products.next().sku());
    }
}
