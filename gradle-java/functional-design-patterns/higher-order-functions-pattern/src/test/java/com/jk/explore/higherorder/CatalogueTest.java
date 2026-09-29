package com.jk.explore.higherorder;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import org.junit.jupiter.api.Test;

class CatalogueTest {

    private final List<Product> all = Product.catalogue();

    @Test
    void passedInTestMatchesTheCopiedLoop() {
        assertEquals(CopyPasteFilters.mugs(all), Catalogue.filter(all, Catalogue.inCategory("mug")));
        assertEquals(CopyPasteFilters.inStock(all), Catalogue.filter(all, Catalogue.inStock()));
    }

    @Test
    void amountOffNeverGoesNegative() {
        assertEquals(0.0, Catalogue.amountOff(5).applyAsDouble(3));
    }

    @Test
    void percentOffRoundsToPence() {
        assertEquals(6.8, Catalogue.percentOff(20).applyAsDouble(8.50));
    }
}
