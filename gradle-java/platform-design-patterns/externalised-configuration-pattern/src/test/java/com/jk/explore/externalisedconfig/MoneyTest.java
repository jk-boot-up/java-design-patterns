package com.jk.explore.externalisedconfig;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Money, and in particular what it does with text from outside the program.
 *
 * <p>The negative case in {@link #minusOneIsAPerfectlyWellFormedNumber()} is the
 * one to read. It is not a bug that {@code "-1"} parses; it is the reason the rest
 * of this project exists.
 */
class MoneyTest {

    @Test
    @DisplayName("pounds and pence agree with each other")
    void poundsAndPence() {
        assertEquals(Money.pence(5000), Money.pounds(50));
        assertEquals("£4.99", Money.pence(499).toString());
        assertEquals("£0.00", Money.zero().toString());
    }

    @Test
    @DisplayName("well-formed text parses, with or without a decimal part")
    void wellFormedTextParses() {
        assertEquals(Money.pounds(50), Money.parse("50").orElseThrow());
        assertEquals(Money.pounds(35), Money.parse("35.00").orElseThrow());
        assertEquals(Money.pence(499), Money.parse("4.99").orElseThrow());
        assertEquals(Money.pence(450), Money.parse("4.5").orElseThrow());
        assertEquals(Money.pounds(35), Money.parse("  35 ").orElseThrow());
    }

    @Test
    @DisplayName("text that is not a number parses to nothing at all")
    void textThatIsNotANumber() {
        assertTrue(Money.parse("fifty").isEmpty());
        assertTrue(Money.parse("").isEmpty());
        assertTrue(Money.parse("50 pounds").isEmpty());
        assertTrue(Money.parse("£50").isEmpty());
        assertTrue(Money.parse(null).isEmpty());
    }

    @Test
    @DisplayName("minus one is a perfectly well-formed number, which is the problem")
    void minusOneIsAPerfectlyWellFormedNumber() {
        Money minusOne = Money.parse("-1").orElseThrow();

        assertEquals(Money.pounds(-1), minusOne);
        assertTrue(minusOne.isNegative());
        assertEquals("-£1.00", minusOne.toString());
        // And here is why it is dangerous: every basket clears it.
        assertTrue(Money.zero().isAtLeast(minusOne));
    }

    @Test
    @DisplayName("isAtLeast is inclusive at the threshold")
    void isAtLeastIsInclusive() {
        assertTrue(Money.pounds(50).isAtLeast(Money.pounds(50)));
        assertTrue(Money.pence(5001).isAtLeast(Money.pounds(50)));
        assertFalse(Money.pence(4999).isAtLeast(Money.pounds(50)));
    }
}
