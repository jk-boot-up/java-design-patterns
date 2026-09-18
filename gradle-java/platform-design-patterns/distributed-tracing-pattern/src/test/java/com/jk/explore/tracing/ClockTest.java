package com.jk.explore.tracing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

/**
 * The scripted clock, which is what makes every other test in this project
 * able to assert an exact number.
 */
class ClockTest {

    @Test
    @DisplayName("a fresh clock is at the start of the request")
    void startsAtZero() {
        assertEquals(0, new Clock.Scripted().now());
    }

    @Test
    @DisplayName("declared work moves time forward by exactly that much")
    void advancesByTheDeclaredDuration() {
        Clock.Scripted clock = new Clock.Scripted();

        clock.advance(120);
        clock.advance(180);

        assertEquals(300, clock.now());
    }

    @Test
    @DisplayName("advance reports the instant the work finished")
    void advanceReturnsTheNewNow() {
        Clock.Scripted clock = new Clock.Scripted();
        clock.advance(120);

        assertEquals(300, clock.advance(180));
    }

    @Test
    @DisplayName("time does not run backwards")
    void refusesToGoBackwards() {
        assertThrows(IllegalArgumentException.class, () -> new Clock.Scripted().advance(-1));
    }
}
