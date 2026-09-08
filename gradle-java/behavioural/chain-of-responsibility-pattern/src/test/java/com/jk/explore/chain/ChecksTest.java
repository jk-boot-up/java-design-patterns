package com.jk.explore.chain;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * Each link on its own.
 *
 * <p>This file is the quiet argument for the pattern. Every test here builds
 * one check and asks it one question — no chain, no other checks, no setup that
 * the check does not care about. In the naive version the fraud rule is the
 * fifth statement of a method, so reaching it means first constructing a
 * deliverable address, a pickable basket and a card with headroom.
 */
class ChecksTest {

    private static CheckoutRequest order(String country, String postcode,
                                         int cardLimit, int fraudScore, int quantity) {
        return new CheckoutRequest("R1",
                List.of(new BasketItem("MON-27", "Monitor", 329, quantity)),
                country, postcode, cardLimit, fraudScore);
    }

    @Test
    @DisplayName("address rejects a country we do not ship to")
    void unservedCountry() {
        Optional<Decision> decision =
                new AddressCheck().check(order("FR", "75001", 2000, 10, 1));

        assertEquals(Outcome.REJECTED, decision.orElseThrow().outcome());
        assertTrue(decision.orElseThrow().reason().contains("FR"));
    }

    @Test
    @DisplayName("address rejects an offshore postcode")
    void offshorePostcode() {
        assertEquals(Outcome.REJECTED,
                new AddressCheck().check(order("GB", "JE3 8QX", 2000, 10, 1))
                        .orElseThrow().outcome());
    }

    @Test
    @DisplayName("address says nothing about an ordinary mainland order")
    void mainlandAddressPassesOn() {
        assertTrue(new AddressCheck().check(order("GB", "M1 4BT", 2000, 10, 1)).isEmpty());
    }

    @Test
    @DisplayName("stock rejects when the warehouse cannot pick the line")
    void notEnoughOnTheShelf() {
        StockCheck check = new StockCheck(Map.of("MON-27", 1));

        assertEquals(Outcome.REJECTED,
                check.check(order("GB", "M1 4BT", 2000, 10, 3)).orElseThrow().outcome());
    }

    @Test
    @DisplayName("fraud rejects at 80 and above")
    void highScoreIsRejected() {
        assertEquals(Outcome.REJECTED,
                new FraudScoreCheck().check(order("GB", "M1 4BT", 2000, 80, 1))
                        .orElseThrow().outcome());
    }

    @Test
    @DisplayName("fraud refers between 55 and 79 — the answer a boolean cannot hold")
    void greyBandIsReferred() {
        assertEquals(Outcome.REFERRED,
                new FraudScoreCheck().check(order("GB", "M1 4BT", 2000, 64, 1))
                        .orElseThrow().outcome());
    }

    @Test
    @DisplayName("fraud says nothing below 55")
    void lowScorePassesOn() {
        assertTrue(new FraudScoreCheck().check(order("GB", "M1 4BT", 2000, 54, 1)).isEmpty());
    }

    @Test
    @DisplayName("payment rejects a total above the card limit")
    void overTheCardLimit() {
        assertEquals(Outcome.REJECTED,
                new PaymentLimitCheck().check(order("GB", "M1 4BT", 250, 10, 1))
                        .orElseThrow().outcome());
    }

    @Test
    @DisplayName("payment says nothing when the total is exactly the limit")
    void exactlyAtTheCardLimit() {
        assertTrue(new PaymentLimitCheck().check(order("GB", "M1 4BT", 329, 10, 1)).isEmpty());
    }
}
