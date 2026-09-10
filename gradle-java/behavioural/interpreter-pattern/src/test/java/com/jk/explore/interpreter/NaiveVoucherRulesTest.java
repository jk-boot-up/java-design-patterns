package com.jk.explore.interpreter;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * The hard-coded rules, with their wrong answers pinned in place.
 *
 * <p>These tests pass, and they assert behaviour that is wrong. That is the
 * point: the cost of writing promotions as Java branches should be stated by
 * the build rather than claimed by a README. Fix {@link NaiveVoucherRules} and
 * these go red, which is exactly right — being broken is its whole job.
 */
class NaiveVoucherRulesTest {

    private static final List<String> LIVE = List.of(
            "SAVE10   | 10 | country is UK and basket over 50",
            "SAVE15   | 15 | country is UK and basket over 100",
            "FREESHIP |  5 | country is UK and items at least 3");

    private final NaiveVoucherRules naive = new NaiveVoucherRules();
    private final PromotionBook book = PromotionBook.fromLines(LIVE);

    @Test
    @DisplayName("on an ordinary order both versions agree, which is why nobody looked")
    void theHappyPathIsCorrect() {
        Order ukBigBasket = new Order(120, "UK", 4, false);

        assertEquals(15, naive.bestPercentFor(ukBigBasket));
        assertEquals(15, book.bestPercentFor(ukBigBasket));
    }

    @Test
    @DisplayName("BUG: an overseas order gets 15% off a promotion it cannot have")
    void givesTheDiscountAway() {
        Order overseas = new Order(120, "US", 2, false);

        // SAVE15 was written without the UK check, so every large basket in the
        // world qualifies. Fifteen percent, every time, with nothing logged.
        assertEquals(15, naive.bestPercentFor(overseas));
        assertEquals(0, book.bestPercentFor(overseas));
    }

    @Test
    @DisplayName("BUG: a shopper who qualifies for free shipping is offered nothing")
    void withholdsTheDiscountItShouldGive() {
        Order returningShopper = new Order(30, "UK", 3, false);

        // FREESHIP carries a first-order check copied in from a promotion that
        // retired last spring. A missing discount looks exactly like a shopper
        // who did not qualify, so nobody reports it.
        assertEquals(0, naive.bestPercentFor(returningShopper));
        assertEquals(5, book.bestPercentFor(returningShopper));
    }

    @Test
    @DisplayName("and it cannot say why it decided anything")
    void hasNothingToPutInTheAuditLog() {
        // There is no equivalent call to write here. The naive version returns
        // a number and keeps its reasoning in the shape of the Java it is made
        // of, so "why did this order get 15% off?" can only be answered by
        // reading the source.
        assertEquals(List.of(
                        "SAVE10 (10% off) applies when country is UK and basket over 50",
                        "SAVE15 (15% off) applies when country is UK and basket over 100"),
                book.reasonsFor(new Order(120, "UK", 1, false)));
    }
}
