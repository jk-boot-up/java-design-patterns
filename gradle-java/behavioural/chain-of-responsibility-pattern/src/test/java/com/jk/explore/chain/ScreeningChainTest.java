package com.jk.explore.chain;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

/**
 * Tests for the chain.
 *
 * <p>A test that says "a Jersey order is rejected" would pass against the naive
 * method just as happily, so it proves nothing about the pattern. The tests
 * here assert the things only a chain gives you: that a link behind a decision
 * never runs, that reordering changes the answer without any check being
 * edited, and that a link nobody in the main source has heard of still works.
 */
class ScreeningChainTest {

    private static final Map<String, Integer> ON_SHELF = Map.of("MON-27", 5, "KEY-01", 20);

    private static CheckoutRequest order(String postcode, int cardLimit, int fraudScore) {
        return new CheckoutRequest("R1", List.of(new BasketItem("MON-27", "Monitor", 329, 1)),
                "GB", postcode, cardLimit, fraudScore);
    }

    private static ScreeningChain standard() {
        return new ScreeningChain("standard", Decision.approved("end of chain", "nobody objected"),
                new AddressCheck(), new StockCheck(ON_SHELF),
                new FraudScoreCheck(), new PaymentLimitCheck());
    }

    @Nested
    @DisplayName("what the chain gives you that four ifs do not")
    class OnlyAChain {

        @Test
        @DisplayName("a link behind the deciding link never runs at all")
        void linksBehindTheDecisionNeverRun() {
            ScreeningReport report = standard().screen(order("SW1A 1AA", 250, 92));

            assertEquals(Outcome.REJECTED, report.outcome());
            assertEquals("fraud-score", report.decision().decidedBy());
            assertEquals(List.of("payment-limit"), report.neverRan());
        }

        @Test
        @DisplayName("the first link stopping means nothing behind it is paid for")
        void aCheapRejectionSkipsEverythingExpensive() {
            ScreeningReport report = standard().screen(order("JE3 8QX", 2000, 10));

            assertEquals("address", report.decision().decidedBy());
            assertEquals(List.of("stock", "fraud-score", "payment-limit"), report.neverRan());
        }

        @Test
        @DisplayName("reordering the links changes the answer, with no check edited")
        void reorderingChangesTheAnswer() {
            CheckoutRequest overLimitAndSuspicious = order("SW1A 1AA", 250, 92);

            ScreeningChain fraudFirst = standard();
            ScreeningChain paymentFirst = new ScreeningChain("payment-first",
                    Decision.approved("end of chain", "nobody objected"),
                    new AddressCheck(), new StockCheck(ON_SHELF),
                    new PaymentLimitCheck(), new FraudScoreCheck());

            assertEquals("fraud-score",
                    fraudFirst.screen(overLimitAndSuspicious).decision().decidedBy());
            assertEquals("payment-limit",
                    paymentFirst.screen(overLimitAndSuspicious).decision().decidedBy());
        }

        @Test
        @DisplayName("a link the chain has never heard of works without changing the chain")
        void aBrandNewLinkJustWorks() {
            ScreeningHandler blockMondays = new ScreeningHandler() {
                @Override
                public String name() {
                    return "no-mondays";
                }

                @Override
                protected Optional<Decision> check(CheckoutRequest request) {
                    return Optional.of(Decision.rejected(name(), "not on a Monday"));
                }
            };

            ScreeningChain chain = new ScreeningChain("with-a-stranger",
                    Decision.approved("end of chain", "nobody objected"),
                    blockMondays, new AddressCheck());

            ScreeningReport report = chain.screen(order("SW1A 1AA", 2000, 10));
            assertEquals("no-mondays", report.decision().decidedBy());
            assertEquals(List.of("address"), report.neverRan());
        }
    }

    @Nested
    @DisplayName("the three answers")
    class ThreeAnswers {

        @Test
        @DisplayName("a score in the grey band is referred, not accepted")
        void greyBandIsReferred() {
            ScreeningReport report = standard().screen(order("M1 4BT", 2000, 64));

            assertEquals(Outcome.REFERRED, report.outcome());
            assertFalse(report.isApproved());
        }

        @Test
        @DisplayName("a clean order reaches the fallback and is approved by it")
        void nobodyObjectsSoTheFallbackDecides() {
            ScreeningReport report = standard().screen(order("M1 4BT", 2000, 10));

            assertTrue(report.isApproved());
            assertEquals("end of chain", report.decision().decidedBy());
            assertEquals(List.of("address", "stock", "fraud-score", "payment-limit"),
                    report.consulted());
            assertTrue(report.neverRan().isEmpty());
        }

        @Test
        @DisplayName("a chain can be wired to refer rather than approve when nobody speaks")
        void theFallbackIsTheWiringsChoice() {
            ScreeningChain cautious = new ScreeningChain("cautious",
                    Decision.referred("end of chain", "nobody took responsibility"),
                    new AddressCheck());

            assertEquals(Outcome.REFERRED, cautious.screen(order("M1 4BT", 2000, 10)).outcome());
        }
    }

    @Test
    @DisplayName("a chain with no links is refused rather than approving everything")
    void anEmptyChainIsRefused() {
        assertThrows(IllegalArgumentException.class, () -> new ScreeningChain(
                "empty", Decision.approved("end of chain", "nobody objected")));
    }
}
