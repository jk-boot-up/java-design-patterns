package com.jk.explore.tracingjaeger;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import com.jk.explore.tracingjaeger.JaegerQuery.HeldSpan;
import com.jk.explore.tracingjaeger.JaegerQuery.HeldTrace;
import com.jk.explore.tracingjaeger.JaegerTracingDemo.PageLoad;
import com.jk.explore.tracingjaeger.JaegerTracingDemo.Shop;
import io.opentelemetry.sdk.trace.samplers.Sampler;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

/**
 * What a real Jaeger holds, asked of it directly, after two real services have talked over
 * real HTTP.
 *
 * <p>One Jaeger is started for the whole class, because starting it is the slow part. Every
 * test uses its own visit id and its own id seed, so the tests cannot see each other's traces.
 * Every wait is a bounded poll on something Jaeger can actually be asked about; there is no
 * sleep anywhere in this file.
 */
class RealJaegerTest {

    private static JaegerServer jaeger;
    private static JaegerQuery held;

    @BeforeAll
    static void startJaeger() {
        assumeTrue(JaegerServer.containerRuntimeAvailable(), "needs a container runtime");
        jaeger = new JaegerServer();
        jaeger.start();
        held = jaeger.query();
    }

    @AfterAll
    static void stopJaeger() {
        if (jaeger != null) {
            jaeger.close();
        }
    }

    @Test
    void theHeaderCarriesOneTraceAcrossTheHopAndJaegerJoinsTheTwoServicesReports() {
        PageLoad load;
        try (Shop shop = Shop.normal(jaeger, 101, true)) {
            load = shop.load("test-forwarded");
            shop.stopPolitely();
        }
        assertEquals(load.sentHeader(), load.receivedHeader());
        assertTrue(load.sentHeader().matches("00-[0-9a-f]{32}-[0-9a-f]{16}-01"), load.sentHeader());
        assertEquals(load.traceId(), load.recommendationsTraceId());

        HeldTrace trace = JaegerTracingDemo.awaitTrace(held, load.traceId(), JaegerTracingDemo.SPANS_PER_PAGE);
        assertEquals(8, trace.spans().size());
        assertEquals(6, trace.spansFrom(ProductPageService.NAME));
        assertEquals(2, trace.spansFrom(RecommendationsService.NAME));
        assertEquals(1, trace.roots());
        HeldSpan answer = trace.named("GET /recommendations").orElseThrow();
        assertEquals("call recommendations", trace.parentOf(answer).orElseThrow().name());
        assertEquals("ranking-model", JaegerTracingDemo.slowestByOwnTime(trace).name());
        assertTrue(trace.named("ranking-model").orElseThrow().durationMicros() >= 340_000);
    }

    @Test
    void withoutTheHeaderOnePageLoadBecomesTwoTracesEachWithItsOwnRoot() {
        PageLoad load;
        try (Shop shop = Shop.normal(jaeger, 102, false)) {
            load = shop.load("test-forgotten");
            shop.stopPolitely();
        }
        assertEquals("none", load.sentHeader());
        assertEquals("none", load.receivedHeader());
        assertNotEquals(load.traceId(), load.recommendationsTraceId());

        HeldTrace page = JaegerTracingDemo.awaitTrace(held, load.traceId(), JaegerTracingDemo.PAGE_SPANS);
        HeldTrace recommendations = JaegerTracingDemo.awaitTrace(held, load.recommendationsTraceId(), JaegerTracingDemo.RECOMMENDATIONS_SPANS);
        assertEquals(1, page.roots());
        assertEquals(1, recommendations.roots());
        assertEquals(0, page.spansFrom(RecommendationsService.NAME));
        assertEquals(0, page.childrenOf(page.named("call recommendations").orElseThrow()).size());
        Poll.until("the visit id to find both halves", () ->
                held.tracesForVisit(ProductPageService.NAME, "test-forgotten").size() == 1
                && held.tracesForVisit(RecommendationsService.NAME, "test-forgotten").size() == 1);
    }

    @Test
    void theSpansAreNotInJaegerWhenTheCustomerHasThePageButArriveInTheNextBatch() {
        try (Shop shop = Shop.normal(jaeger, 103, true)) {
            PageLoad load = shop.load("test-late");
            assertFalse(held.trace(load.traceId()).isPresent(), "nothing is sent until the batch is due");
            HeldTrace trace = JaegerTracingDemo.awaitTrace(held, load.traceId(), JaegerTracingDemo.SPANS_PER_PAGE);
            assertEquals(8, trace.spans().size());
            shop.stopPolitely();
        }
    }

    @Test
    void aDroppedTraceSaysSoInTheHeaderAndNeitherServiceRecordsIt() {
        List<PageLoad> loads = new ArrayList<>();
        try (Shop shop = new Shop(jaeger, 4, Sampler.parentBased(Sampler.traceIdRatioBased(0.25)),
                ProductPageService.Work.NONE, 0, 0, 0, true)) {
            for (int i = 1; i <= 20; i++) {
                loads.add(shop.load("test-sampled-" + i));
            }
            shop.stopPolitely();
        }
        List<PageLoad> kept = loads.stream().filter(PageLoad::sampled).toList();
        // The ids come from a fixed seed, so the sampler's choices are the same on every run.
        assertEquals(6, kept.size());
        for (PageLoad k : kept) {
            assertTrue(k.receivedHeader().endsWith("-01"));
            HeldTrace t = JaegerTracingDemo.awaitTrace(held, k.traceId(), JaegerTracingDemo.SPANS_PER_PAGE);
            assertEquals(2, t.spansFrom(RecommendationsService.NAME));
        }
        for (PageLoad d : loads) {
            if (!d.sampled()) {
                assertTrue(d.receivedHeader().endsWith("-00"));
                assertFalse(held.trace(d.traceId()).isPresent());
            }
        }
    }

    @Test
    void aClockThatIsOffPutsTheChildBeforeItsParentAndJaegerOnlyWarns() {
        PageLoad load;
        try (Shop shop = new Shop(jaeger, 105, Sampler.parentBased(Sampler.alwaysOn()), ProductPageService.Work.NORMAL,
                60, 340, -3000, true)) {
            load = shop.load("test-clock");
            shop.stopPolitely();
        }
        HeldTrace trace = JaegerTracingDemo.awaitTrace(held, load.traceId(), JaegerTracingDemo.SPANS_PER_PAGE);
        HeldSpan call = trace.named("call recommendations").orElseThrow();
        HeldSpan answer = trace.named("GET /recommendations").orElseThrow();
        long earlyMillis = (call.startMicros() - answer.startMicros()) / 1000;
        assertTrue(earlyMillis > 2000 && earlyMillis < 3000, "early by " + earlyMillis);
        assertEquals(call.spanId(), answer.parentSpanId());
        assertEquals(1, trace.roots());
        assertTrue(trace.warnings().stream().anyMatch(w -> w.startsWith("clock skew adjustment disabled")), trace.warnings().toString());
    }

    @Test
    void aServiceKilledBeforeItsNextBatchNeverSendsItsSpans() {
        PageLoad load;
        try (Shop shop = Shop.normal(jaeger, 106, true)) {
            load = shop.load("test-crash");
            shop.recommendations.kill();
            shop.stopPolitely();
        }
        HeldTrace trace = JaegerTracingDemo.awaitTrace(held, load.traceId(), JaegerTracingDemo.PAGE_SPANS);
        assertEquals(6, trace.spans().size());
        assertEquals(0, trace.spansFrom(RecommendationsService.NAME));
    }

    @Test
    void jaegerSaysItKeepsSpansInMemory() {
        assertTrue(jaeger.storageLine().contains("memory storage"), jaeger.storageLine());
    }
}
