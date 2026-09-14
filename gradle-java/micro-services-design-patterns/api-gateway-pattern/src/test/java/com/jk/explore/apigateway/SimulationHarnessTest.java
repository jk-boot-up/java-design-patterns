package com.jk.explore.apigateway;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The three-class harness the whole category runs on.
 *
 * It is worth testing for one reason: every other test in this project trusts it
 * to make failure and time behave the same way twice.
 */
class SimulationHarnessTest {

    @Test
    void theClockOnlyMovesWhenSomethingMovesIt() {
        SimulatedClock clock = new SimulatedClock();

        assertEquals(0, clock.millis());
        clock.advance(150);
        assertEquals(150, clock.millis());
        assertThrows(IllegalArgumentException.class, () -> clock.advance(-1));
    }

    @Test
    void aRemoteCallCostsTimeAndSaysSoInTheLog() {
        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        RemoteCall<String, String> call =
                new RemoteCall<>("Catalog", 40, sku -> "answer for " + sku, clock, log);

        assertEquals("answer for SKU-1234", call.invoke("SKU-1234"));
        assertEquals(40, clock.millis());
        assertEquals(1, log.size());
        assertEquals("OK", log.entries().get(0).outcome());
        assertEquals(40, log.entries().get(0).durationMillis());
    }

    @Test
    void aScriptedFailureFailsExactlyAsManyTimesAsItWasTold() {
        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        RemoteCall<String, String> call =
                new RemoteCall<>("Payments", 40, sku -> "charged", clock, log);

        call.failNext(2);

        assertThrows(ServiceUnavailableException.class, () -> call.invoke("x"));
        assertThrows(ServiceUnavailableException.class, () -> call.invoke("x"));
        assertEquals("charged", call.invoke("x"), "fail twice, then succeed");
        assertEquals(3, call.invocations());
    }

    @Test
    void aFailedCallStillTakesAsLongAsASuccessfulOne() {
        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        RemoteCall<String, String> call =
                new RemoteCall<>("Recommendations", 40, sku -> "suggestions", clock, log);

        call.failNext(1);
        assertThrows(ServiceUnavailableException.class, () -> call.invoke("x"));

        assertEquals(40, clock.millis(),
                "waiting for an answer that never comes is the expensive kind of "
                        + "failure, and the clock has to show it");
    }

    @Test
    void theTimelineIsOrderedByWhenEachCallStarted() {
        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);

        // Written in the order an enclosing call and its inner call would be
        // written: the inner one finishes, and is logged, first.
        log.record(100, 110, "Catalog", "OK", "inner");
        log.record(0, 240, "Gateway", "OK", "outer");

        assertEquals(java.util.List.of("Gateway", "Catalog"), log.services());
        assertEquals(240, log.elapsedMillis());
        assertTrue(log.timeline().indexOf("Gateway") < log.timeline().indexOf("Catalog"));
    }

    @Test
    void aDecisionIsLoggedWithoutCostingTime() {
        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        clock.advance(75);

        log.note("Gateway", "DEGRADED", "no suggestions");

        assertEquals(75, clock.millis(), "deciding something takes no network time");
        assertEquals(0, log.entries().get(0).durationMillis());
        assertEquals(1, log.countFor("Gateway"));
    }

    @Test
    void theDemoRunsWithoutFailing() {
        ProductPageDemo.main(new String[0]);
    }
}
