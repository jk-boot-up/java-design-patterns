package com.jk.explore.interpreter;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** The promotions the shop is running, read from text. */
class PromotionBookTest {

    private static final List<String> LIVE = List.of(
            "SAVE10   | 10 | country is UK and basket over 50",
            "SAVE15   | 15 | country is UK and basket over 100",
            "FREESHIP |  5 | country is UK and items at least 3");

    private final PromotionBook book = PromotionBook.fromLines(LIVE);

    @Test
    @DisplayName("the best matching promotion wins")
    void bestPercentIsTheLargestThatApplies() {
        assertEquals(15, book.bestPercentFor(new Order(120, "UK", 4, false)));
        assertEquals(10, book.bestPercentFor(new Order(60, "UK", 1, false)));
        assertEquals(5, book.bestPercentFor(new Order(30, "UK", 3, false)));
    }

    @Test
    @DisplayName("an order that qualifies for nothing gets nothing")
    void noMatchMeansNoDiscount() {
        assertEquals(0, book.bestPercentFor(new Order(120, "US", 2, false)));
        assertEquals(0, book.bestPercentFor(new Order(10, "UK", 1, true)));
    }

    @Test
    @DisplayName("the book can say why, in the words the rule was written in")
    void reasonsComeStraightOutOfTheTrees() {
        List<String> reasons = book.reasonsFor(new Order(30, "UK", 3, false));

        assertEquals(List.of("FREESHIP (5% off) applies when country is UK and items at least 3"),
                reasons);
    }

    @Test
    @DisplayName("a promotion nobody anticipated needs no new class")
    void newRulesAreTextRatherThanCode() {
        // The shape of this rule -- an "or" at the top -- appears nowhere in
        // the promotions the book was built with. Adding it is one line.
        List<String> withNewOffer = new ArrayList<>(LIVE);
        withNewOffer.add("BIGBASKET | 20 | basket over 200 or items at least 10");

        PromotionBook friday = PromotionBook.fromLines(withNewOffer);

        assertEquals(20, friday.bestPercentFor(new Order(90, "UK", 12, false)));
        assertEquals(20, friday.bestPercentFor(new Order(250, "US", 1, false)));
        // ...and the promotions that were already running are untouched.
        assertEquals(10, friday.bestPercentFor(new Order(60, "UK", 1, false)));
    }

    @Test
    @DisplayName("a promotion with a typo in it never reaches the checkout")
    void abadLineStopsTheBookBeingBuilt() {
        List<String> broken = List.of("OOPS | 10 | country is UK and basket ovr 50");

        IllegalArgumentException e = assertThrows(IllegalArgumentException.class,
                () -> PromotionBook.fromLines(broken));

        assertTrue(e.getMessage().contains("basket ovr 50"), e.getMessage());
    }
}
