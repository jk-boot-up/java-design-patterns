package com.jk.explore.specification;

import com.jk.explore.specification.domain.*;
import org.junit.jupiter.api.Test;

import java.util.List;

import static com.jk.explore.specification.SpecificationDemo.*;
import static org.junit.jupiter.api.Assertions.*;

class SpecificationTest {

    @Test
    void cheapAndAvailableSelectsTheRightProducts() {
        assertEquals(List.of(MUG, TEA), new Catalogue(SHELF).select(Products.cheapAndAvailable()));
    }

    @Test
    void theLimitIsStrict() {
        assertFalse(Products.priceUnder(1000).isSatisfiedBy(TENNER));
        assertTrue(Products.priceUnder(1000).isSatisfiedBy(MUG));
    }

    @Test
    void andOrNotBehaveLikeTheirLogic() {
        var inStock = Products.inStock();
        var onSale = Products.onSale();
        for (Product p : SHELF) {
            assertEquals(inStock.isSatisfiedBy(p) && onSale.isSatisfiedBy(p), inStock.and(onSale).isSatisfiedBy(p));
            assertEquals(inStock.isSatisfiedBy(p) || onSale.isSatisfiedBy(p), inStock.or(onSale).isSatisfiedBy(p));
            assertEquals(!inStock.isSatisfiedBy(p), inStock.not().isSatisfiedBy(p));
        }
    }

    @Test
    void deMorganHolds() {
        var a = Products.inStock();
        var b = Products.onSale();
        for (Product p : SHELF) {
            assertEquals(a.and(b).not().isSatisfiedBy(p), a.not().or(b.not()).isSatisfiedBy(p));
        }
    }

    @Test
    void aRuleDescribesItselfInWords() {
        assertEquals("((in stock and under £10) and not discontinued)", Products.cheapAndAvailable().describe());
    }

    @Test
    void unmetNamesOnlyTheFailingParts() {
        var rule = Products.cheapAndAvailable();
        assertEquals(List.of(), rule.unmet(MUG));
        assertEquals(List.of("under £10"), rule.unmet(TENNER));
        assertEquals(List.of("not discontinued"), rule.unmet(OLD));
        assertEquals(List.of("in stock"), rule.unmet(GONE));
    }

    @Test
    void anOrThatIsSatisfiedReportsNothingUnmet() {
        var rule = Products.inStock().or(Products.onSale());
        assertEquals(List.of(), rule.unmet(MACHINE));
        assertEquals(List.of("in stock", "on sale"), rule.unmet(new Product("X", "x", 1, false, false, false)));
    }

    @Test
    void aSpecificationLooksAtEveryProduct() {
        List<Product> big = new java.util.ArrayList<>();
        for (int i = 0; i < 1000; i++) big.add(new Product("S" + i, "mug", i, true, false, false));
        Catalogue c = new Catalogue(big);
        assertEquals(10, c.select(Products.priceUnder(10)).size());
        assertEquals(1000, c.examined());
    }
}
