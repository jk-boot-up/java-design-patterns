package com.jk.explore.iterator;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** What a caller of the catalogue is entitled to rely on. */
class ProductCatalogueTest {

    private ProductCatalogue catalogue() {
        return new ProductCatalogue(CatalogueFeed.sampleShop());
    }

    @Test
    @DisplayName("for-each visits every product, in catalogue order, once")
    void forEachVisitsEveryProduct() {
        List<String> seen = new ArrayList<>();
        for (Product product : catalogue()) {
            seen.add(product.sku());
        }

        assertEquals(List.of("SKU-001", "SKU-002", "SKU-003", "SKU-004",
                        "SKU-005", "SKU-006", "SKU-007", "SKU-008"),
                seen);
    }

    @Test
    @DisplayName("the walk crosses page boundaries without the caller knowing")
    void walkCrossesPageBoundaries() {
        int total = 0;
        for (Product ignored : catalogue()) {
            total++;
        }

        // 8 products at 3 per page is 2 full pages and a part page. If the
        // iterator lost its place at a boundary this number would be 3 or 6.
        assertEquals(8, total);
        assertTrue(total > CatalogueFeed.PAGE_SIZE, "the test is pointless on a single page");
    }

    @Test
    @DisplayName("each call to iterator() starts a fresh walk")
    void eachIteratorStartsFresh() {
        ProductCatalogue catalogue = catalogue();

        int first = 0;
        for (Product ignored : catalogue) {
            first++;
        }
        int second = 0;
        for (Product ignored : catalogue) {
            second++;
        }

        assertEquals(first, second, "the second loop saw a different catalogue");
        assertEquals(8, second);
    }
}
