package com.jk.explore.specification;

import com.jk.explore.specification.naive.NaiveShop;
import org.junit.jupiter.api.Test;

import java.util.List;

import static com.jk.explore.specification.SpecificationDemo.*;
import static org.junit.jupiter.api.Assertions.*;

/** Documents the drift between three copies of one rule. */
class NaiveVersionTest {

    @Test
    void theThreeCopiesDisagree() {
        assertEquals(List.of(MUG, TEA), SHELF.stream().filter(NaiveShop::showOnSearchPage).toList());
        assertEquals(List.of(MUG, TENNER, OLD, TEA), SHELF.stream().filter(NaiveShop::eligibleForPromotion).toList());
        assertEquals(List.of(MUG, TEA), SHELF.stream().filter(NaiveShop::qualifiesForFreeShipping).toList());
    }
}
