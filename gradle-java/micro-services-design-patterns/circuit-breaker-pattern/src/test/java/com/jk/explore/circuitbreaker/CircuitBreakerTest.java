package com.jk.explore.circuitbreaker;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** The three states and the four transitions between them, one test each. */
class CircuitBreakerTest {

    private static final int THRESHOLD = 3;
    private static final long RESET_AFTER = 5_000;

    private SimulatedClock clock;
    private CallLog log;
    private CircuitBreaker breaker;

    @BeforeEach
    void setUp() {
        clock = new SimulatedClock();
        log = new CallLog(clock);
        breaker = new CircuitBreaker("Recommendations", THRESHOLD, RESET_AFTER, clock, log);
    }

    private void failOnce() {
        assertThrows(ServiceUnavailableException.class,
                () -> breaker.call(() -> { throw new ServiceUnavailableException("Recommendations"); }));
    }

    @Test
    @DisplayName("a new breaker is closed, which is the healthy state")
    void itStartsClosed() {
        assertEquals(BreakerState.CLOSED, breaker.state());
    }

    @Test
    @DisplayName("while closed, calls go through and answers come back")
    void closedLetsCallsThrough() {
        assertEquals("ok", breaker.call(() -> "ok"));
        assertEquals(BreakerState.CLOSED, breaker.state());
    }

    @Test
    @DisplayName("two failures are not enough to trip a breaker set to three")
    void itToleratesFailuresBelowTheThreshold() {
        failOnce();
        failOnce();

        assertEquals(BreakerState.CLOSED, breaker.state());
        assertEquals(2, breaker.consecutiveFailures());
    }

    @Test
    @DisplayName("the third failure in a row opens the breaker")
    void theThresholdOpensIt() {
        failOnce();
        failOnce();
        failOnce();

        assertEquals(BreakerState.OPEN, breaker.state());
    }

    @Test
    @DisplayName("one success resets the count, because a bad moment is not an outage")
    void successResetsTheCount() {
        failOnce();
        failOnce();
        breaker.call(() -> "ok");
        failOnce();
        failOnce();

        assertEquals(BreakerState.CLOSED, breaker.state(),
                "four failures overall, never three in a row");
    }

    @Test
    @DisplayName("while open, the call is refused without the service being touched")
    void openMakesNoCall() {
        failOnce();
        failOnce();
        failOnce();
        int callsBefore = breaker.callsMade();

        assertThrows(CircuitOpenException.class, () -> breaker.call(() -> "never runs"));
        assertEquals(callsBefore, breaker.callsMade());
        assertEquals(1, breaker.callsRefused());
    }

    @Test
    @DisplayName("a refusal is instant, which is the whole benefit")
    void aRefusalCostsNoTime() {
        failOnce();
        failOnce();
        failOnce();
        long before = clock.millis();

        assertThrows(CircuitOpenException.class, () -> breaker.call(() -> "never runs"));

        assertEquals(before, clock.millis());
    }

    @Test
    @DisplayName("it stays open for the full reset wait, right up to the last millisecond")
    void itStaysOpenForTheWholeWait() {
        failOnce();
        failOnce();
        failOnce();

        clock.advance(RESET_AFTER - 1);
        assertThrows(CircuitOpenException.class, () -> breaker.call(() -> "never runs"));
        assertEquals(BreakerState.OPEN, breaker.state());
    }

    @Test
    @DisplayName("after the wait, exactly one call is let through")
    void afterTheWaitItProbes() {
        failOnce();
        failOnce();
        failOnce();
        clock.advance(RESET_AFTER);

        assertEquals("recovered", breaker.call(() -> "recovered"));
        assertEquals(BreakerState.CLOSED, breaker.state());
        assertEquals(0, breaker.consecutiveFailures());
    }

    @Test
    @DisplayName("if the probe fails the breaker opens again for another full wait")
    void aFailedProbeReopensIt() {
        failOnce();
        failOnce();
        failOnce();
        clock.advance(RESET_AFTER);

        failOnce();   // the probe

        assertEquals(BreakerState.OPEN, breaker.state());
        assertThrows(CircuitOpenException.class, () -> breaker.call(() -> "never runs"));

        clock.advance(RESET_AFTER);
        assertEquals("recovered", breaker.call(() -> "recovered"),
                "the wait restarted from the failed probe, not from the original trip");
    }

    @Test
    @DisplayName("a single failed probe does not need the threshold again to reopen")
    void oneFailedProbeIsEnough() {
        failOnce();
        failOnce();
        failOnce();
        clock.advance(RESET_AFTER);
        failOnce();

        assertEquals(BreakerState.OPEN, breaker.state());
    }

    @Test
    @DisplayName("the timeline names every decision the breaker made")
    void theDecisionsAreVisible() {
        failOnce();
        failOnce();
        failOnce();
        assertThrows(CircuitOpenException.class, () -> breaker.call(() -> "never runs"));
        clock.advance(RESET_AFTER);
        breaker.call(() -> "recovered");

        String timeline = log.timeline();
        assertTrue(timeline.contains("OPENED"), timeline);
        assertTrue(timeline.contains("REFUSED"), timeline);
        assertTrue(timeline.contains("HALF-OPEN"), timeline);
        assertTrue(timeline.contains("CLOSED"), timeline);
    }
}
