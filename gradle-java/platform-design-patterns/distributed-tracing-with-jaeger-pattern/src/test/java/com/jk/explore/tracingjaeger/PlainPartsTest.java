package com.jk.explore.tracingjaeger;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.jk.explore.tracingjaeger.JaegerQuery.HeldSpan;
import com.jk.explore.tracingjaeger.JaegerQuery.HeldTrace;
import io.opentelemetry.sdk.common.Clock;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

/**
 * The parts that need nothing installed: the ids, the clock that is off, and the words the demo
 * uses to describe what it reads back from Jaeger.
 */
class PlainPartsTest {

    @Test
    void theSameSeedGivesTheSameIdsAndEachIdHasTheLengthTheHeaderNeeds() {
        SeededIds a = new SeededIds(2);
        SeededIds b = new SeededIds(2);
        String trace = a.generateTraceId();
        assertEquals(trace, b.generateTraceId());
        assertEquals(32, trace.length());
        String span = a.generateSpanId();
        assertEquals(16, span.length());
        assertNotEquals(span, a.generateSpanId());
        assertTrue(trace.matches("[0-9a-f]{32}"));
    }

    @Test
    void aClockThatIsOffMovesTheWallClockButNotTheStopwatch() {
        Clock real = Clock.getDefault();
        Telemetry.ClockOffBy slow = new Telemetry.ClockOffBy(real, -3000);
        long difference = real.now() - slow.now();
        assertTrue(Math.abs(difference - 3_000_000_000L) < 100_000_000L, "difference " + difference);
        long stopwatch = Math.abs(real.nanoTime() - slow.nanoTime());
        assertTrue(stopwatch < 100_000_000L, "stopwatch " + stopwatch);
    }

    @Test
    void theHeaderIsReadFieldByField() {
        assertEquals("version 00, trace id, the caller's span id, flags 01, which means sampled.",
                JaegerTracingDemo.describeHeader("00-bfc846100bfc1e42987bbcbfdd7e532f-b9f24f7bae4a6586-01"));
        assertEquals("version 00, trace id, the caller's span id, flags 00, which means not sampled.",
                JaegerTracingDemo.describeHeader("00-e474c66a4b98b030dbef19fc8e7b845f-ebb1ae25f75e1f5e-00"));
        assertEquals(55, "00-bfc846100bfc1e42987bbcbfdd7e532f-b9f24f7bae4a6586-01".length());
    }

    @Test
    void jaegersWarningKeepsItsWordsAndRoundsItsAmount() {
        assertEquals("clock skew adjustment disabled; not applying calculated delta of about 3 seconds",
                JaegerTracingDemo.describeWarning(List.of("clock skew adjustment disabled; not applying calculated delta of 2.961255479s")));
        assertEquals("none", JaegerTracingDemo.describeWarning(List.of()));
    }

    @Test
    void timingsAreDescribedRatherThanPrinted() {
        assertEquals("between 2 and 3 seconds", JaegerTracingDemo.describeEarly(2882));
        assertEquals("more than 2 seconds after the customer had the page", JaegerTracingDemo.describeLateness(4131));
    }

    @Test
    void theTreeFollowsTheParentLinksAndOwnTimeLeavesOutTheChildren() {
        HeldTrace trace = new HeldTrace("t", List.of(
                new HeldSpan("a", null, "GET /product/A-2231", "product-page", 0, 900_000),
                new HeldSpan("b", "a", "call recommendations", "product-page", 100_000, 500_000),
                new HeldSpan("c", "b", "GET /recommendations", "recommendations", 150_000, 400_000),
                new HeldSpan("d", "c", "ranking-model", "recommendations", 180_000, 340_000)), List.of());
        List<String> tree = JaegerTracingDemo.tree(trace);
        assertEquals(4, tree.size());
        assertTrue(tree.get(3).startsWith("      ranking-model"), tree.get(3));
        assertEquals(400_000, JaegerTracingDemo.ownMicros(trace, trace.named("GET /product/A-2231").orElseThrow()));
        assertEquals(60_000, JaegerTracingDemo.ownMicros(trace, trace.named("GET /recommendations").orElseThrow()));
        assertEquals("GET /product/A-2231", JaegerTracingDemo.slowestByOwnTime(trace).name());
        assertEquals(1, trace.roots());
        assertEquals(2, trace.servicesCount());
    }

    @Test
    void bothServicesAnswerInNameColonValueLines() {
        Map<String, String> fields = Http.fields("trace-id: abc\nsampled: true\n");
        assertEquals("abc", fields.get("trace-id"));
        assertEquals("true", fields.get("sampled"));
    }

    @Test
    void theNoRuntimeAdviceTellsABeginnerWhatToDo() {
        assertTrue(JaegerServer.NO_RUNTIME_ADVICE.contains("Start Docker Desktop"));
        assertTrue(JaegerServer.NO_RUNTIME_ADVICE.contains("./gradlew run"));
    }
}
