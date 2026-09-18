package com.jk.explore.tracing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The third item on the bill, which is arithmetic rather than opinion.
 *
 * <p>A million requests at one per cent leaves ten thousand traces kept and nine
 * hundred and ninety thousand gone. The last test is the one worth reading: the
 * request somebody actually complains about was discarded, and it was discarded
 * before anybody could know it would matter.
 */
class SamplerTest {

    @Test
    @DisplayName("one trace in a hundred is kept")
    void keepsOneInAHundred() {
        Sampler sampler = new Sampler(100);
        for (int i = 0; i < 1_000; i++) {
            sampler.keep();
        }

        assertEquals(1_000, sampler.seen());
        assertEquals(10, sampler.kept());
        assertEquals(990, sampler.discarded());
    }

    @Test
    @DisplayName("a million requests leaves ten thousand traces")
    void theFiguresTheDemoQuotes() {
        Sampler sampler = new Sampler(100);
        for (int i = 0; i < 1_000_000; i++) {
            sampler.keep();
        }

        assertEquals(10_000, sampler.kept());
        assertEquals(990_000, sampler.discarded());
    }

    @Test
    @DisplayName("kept plus discarded is everything that arrived")
    void nothingIsUnaccountedFor() {
        Sampler sampler = new Sampler(7);
        for (int i = 0; i < 50; i++) {
            sampler.keep();
        }

        assertEquals(sampler.seen(), sampler.kept() + sampler.discarded());
    }

    @Test
    @DisplayName("the first request is always kept")
    void firstIsKept() {
        assertTrue(new Sampler(100).keep());
    }

    @Test
    @DisplayName("the request somebody complains about is probably gone")
    void theComplaintIsNotRecoverable() {
        Sampler sampler = new Sampler(100);

        assertFalse(sampler.wouldHaveKept(862_144));
        assertTrue(sampler.wouldHaveKept(862_101));
    }

    @Test
    @DisplayName("keeping everything is a legal setting, and an expensive one")
    void oneInOneKeepsEverything() {
        Sampler sampler = new Sampler(1);
        for (int i = 0; i < 10; i++) {
            assertTrue(sampler.keep());
        }

        assertEquals(10, sampler.kept());
        assertEquals(0, sampler.discarded());
    }

    @Test
    @DisplayName("you cannot keep one trace in zero")
    void rejectsANonsenseRate() {
        assertThrows(IllegalArgumentException.class, () -> new Sampler(0));
    }
}
