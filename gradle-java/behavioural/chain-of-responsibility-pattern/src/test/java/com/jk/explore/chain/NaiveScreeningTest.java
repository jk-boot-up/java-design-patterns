package com.jk.explore.chain;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * The two bugs in the naive version, pinned down as tests.
 *
 * <p>These pass. They are not describing broken code — they are describing code
 * that works exactly as written, and where what it was written to do is the
 * problem.
 */
class NaiveScreeningTest {

    private static final Map<String, Integer> ON_SHELF = Map.of("MON-27", 5, "DESK-02", 2);

    private final NaiveScreening naive = new NaiveScreening(ON_SHELF);

    @Test
    @DisplayName("an order that is both over the limit and suspicious is reported as the card")
    void theFirstCheckToFireOwnsTheMessage() {
        CheckoutRequest bothAreTrue = new CheckoutRequest("R2001",
                List.of(new BasketItem("MON-27", "Monitor", 329, 1)),
                "GB", "SW1A 1AA", 250, 92);

        NaiveScreening.Result result = naive.validate(bothAreTrue);

        assertFalse(result.accepted());
        assertTrue(result.message().contains("card"));
        // The risk score of 92 is never mentioned, because the method had
        // already returned by the time anything looked at it.
        assertFalse(result.message().contains("92"));
    }

    @Test
    @DisplayName("the grey band is accepted, because a boolean has nowhere else to put it")
    void theThirdAnswerIsLost() {
        CheckoutRequest greyBand = new CheckoutRequest("R2003",
                List.of(new BasketItem("MON-27", "Monitor", 329, 1)),
                "GB", "M1 4BT", 2000, 64);

        assertTrue(naive.validate(greyBand).accepted());
    }

    @Test
    @DisplayName("the copied trade method lost the address check as well as the card check")
    void theCopyDrifted() {
        CheckoutRequest jerseyTradeOrder = new CheckoutRequest("R2004",
                List.of(new BasketItem("DESK-02", "Standing desk", 180, 2)),
                "GB", "JE2 3AB", 0, 20);

        assertFalse(naive.validate(jerseyTradeOrder).accepted());   // the standard method catches it
        assertTrue(naive.validateTradeAccount(jerseyTradeOrder).accepted());  // the copy does not
    }

    @Test
    @DisplayName("for a single market with fixed rules it is simply correct")
    void itIsNotAStrawMan() {
        CheckoutRequest ordinary = new CheckoutRequest("R2005",
                List.of(new BasketItem("MON-27", "Monitor", 329, 1)),
                "GB", "M1 4BT", 2000, 10);

        assertEquals(new NaiveScreening.Result(true, "nothing objected"), naive.validate(ordinary));
    }
}
