package com.jk.explore.flyweight;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotSame;

class NaiveListingBadgeTest {

    @Test
    void twoListingsOfTheSameTypeGetTwoSeparateBadgeObjects() {
        NaiveListingBadge first = new NaiveListingBadge(BadgeType.SALE, "LST-1002");
        NaiveListingBadge second = new NaiveListingBadge(BadgeType.SALE, "LST-1003");

        assertNotSame(first, second);
    }

    @Test
    void eachNaiveBadgeCarriesItsOwnFullCopyOfTheArtwork() {
        NaiveListingBadge first = new NaiveListingBadge(BadgeType.SALE, "LST-1002");
        NaiveListingBadge second = new NaiveListingBadge(BadgeType.SALE, "LST-1003");

        assertEquals(64 * 1024, first.artworkBytes());
        assertEquals(64 * 1024, second.artworkBytes());
    }

    @Test
    void renderMatchesTheFlyweightEquivalentForTheSameInputs() {
        NaiveListingBadge naive = new NaiveListingBadge(BadgeType.NEW, "LST-1001");
        BadgeStyle flyweight = BadgeStyleFactory.styleFor(BadgeType.NEW);

        assertEquals(flyweight.render("LST-1001", null), naive.render());
    }
}
