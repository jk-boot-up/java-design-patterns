package com.jk.explore.iterator;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * These tests pin the naive browser's bugs in place rather than fixing them.
 * They exist so the "before" picture is not just a story -- you can run it.
 */
class NaiveCatalogueBrowserTest {

    private NaiveCatalogueBrowser browser() {
        return new NaiveCatalogueBrowser(CatalogueFeed.sampleShop());
    }

    @Test
    @DisplayName("the carefully written loop is right")
    void allProductsIsCorrect() {
        assertEquals(8, browser().allProducts().size());
    }

    @Test
    @DisplayName("the copy that caps the page count silently loses products")
    void countProductsStopsEarly() {
        assertEquals(8, browser().allProducts().size());
        assertEquals(8, browser().countProducts(),
                "a 3-page cap happens to cover 8 products; grow the catalogue and this breaks");
    }

    @Test
    @DisplayName("the copy that starts at page 1 misses the cheapest product")
    void findCheapestMissesTheFirstPage() {
        Product cheapest = browser().findCheapest();

        // The real cheapest is the £4 pair of socks, SKU-002 -- and SKU-002 is
        // on page 0, the one page this method never asks for. What it returns
        // instead is the £8 mug, the cheapest thing it can actually see.
        Product trueCheapest = null;
        for (Product product : new ProductCatalogue(CatalogueFeed.sampleShop())) {
            if (trueCheapest == null || product.priceInPounds() < trueCheapest.priceInPounds()) {
                trueCheapest = product;
            }
        }

        assertEquals("SKU-002", trueCheapest.sku());
        assertEquals(4, trueCheapest.priceInPounds());

        assertEquals("SKU-005", cheapest.sku(), "the naive method returns the cheapest it can see");
        assertNotEquals(trueCheapest.sku(), cheapest.sku(),
                "if these ever match, the off-by-one has been fixed and the lesson is gone");
    }

    @Test
    @DisplayName("the same walk through the catalogue, written once, is right")
    void thePatternGetsItRight() {
        int count = 0;
        Product cheapest = null;
        for (Product product : new ProductCatalogue(CatalogueFeed.sampleShop())) {
            count++;
            if (cheapest == null || product.priceInPounds() < cheapest.priceInPounds()) {
                cheapest = product;
            }
        }

        assertEquals(8, count);
        assertEquals("SKU-002", cheapest.sku());
    }
}
