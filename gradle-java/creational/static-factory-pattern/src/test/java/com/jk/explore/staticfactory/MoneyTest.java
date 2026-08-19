package com.jk.explore.staticfactory;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.params.provider.Arguments.arguments;

import java.util.stream.Stream;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

@DisplayName("Money — the same argument type, two different meanings")
class MoneyTest {

    @Test
    @DisplayName("pounds() and pence() take one number each and cannot be confused")
    void namesDisambiguateTheUnit() {
        // Two constructors taking a single number could not both exist.
        assertAll(
                () -> assertEquals("£5.00", Money.pounds(5).toString()),
                () -> assertEquals("£0.05", Money.pence(5).toString()));
    }

    @Test
    @DisplayName("zero() is one shared instance, not a fresh object each time")
    void zeroIsShared() {
        assertAll(
                () -> assertSame(Money.zero(), Money.zero()),
                // The factory routes any zero amount to the same instance.
                () -> assertSame(Money.zero(), Money.pounds(0)),
                () -> assertSame(Money.zero(), Money.pence(0)));
    }

    static Stream<Arguments> texts() {
        return Stream.of(
                arguments("£12.50", 1250L),
                arguments("12.50", 1250L),
                arguments("£1,250.50", 125050L),
                arguments("  £0.00  ", 0L));
    }

    @ParameterizedTest(name = "parse({0}) -> {1}p")
    @MethodSource("texts")
    void parseReadsBackWhatToStringWrites(String text, long expectedPence) {
        assertEquals(expectedPence, Money.parse(text).asPence());
    }

    @Test
    @DisplayName("a printed amount can be parsed straight back")
    void roundTrips() {
        Money original = Money.pounds(1250.50);

        assertEquals(original, Money.parse(original.toString()));
    }

    @Test
    @DisplayName("nonsense text is refused, and the message shows it")
    void parseRejectsNonsense() {
        IllegalArgumentException e = assertThrows(IllegalArgumentException.class,
                () -> Money.parse("free"));

        assertEquals("not an amount of money: \"free\"", e.getMessage());
    }

    @Test
    @DisplayName("arithmetic stays in whole pence, so nothing drifts")
    void arithmeticIsExact() {
        Money total = Money.zero();
        for (int i = 0; i < 10; i++) {
            total = total.plus(Money.pounds(0.10));
        }

        assertEquals(Money.pounds(1.00), total);
    }

    @Test
    @DisplayName("percent() rounds to the nearest penny")
    void percentRounds() {
        assertAll(
                () -> assertEquals(Money.pence(1250), Money.pounds(125).percent(10)),
                // 12.5% of £1.01 is 12.625p, which rounds to 13p.
                () -> assertEquals(Money.pence(13), Money.pence(101).percent(13)));
    }

    @Test
    @DisplayName("cappedAt() never returns more than the ceiling")
    void cappedAtLimits() {
        assertAll(
                () -> assertEquals(Money.pounds(3), Money.pounds(5).cappedAt(Money.pounds(3))),
                () -> assertEquals(Money.pounds(5), Money.pounds(5).cappedAt(Money.pounds(9))));
    }
}
