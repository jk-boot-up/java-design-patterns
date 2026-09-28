package com.jk.explore.tracingjaeger;

import com.jk.explore.tracingjaeger.JaegerQuery.HeldSpan;
import com.jk.explore.tracingjaeger.JaegerQuery.HeldTrace;
import io.opentelemetry.sdk.OpenTelemetrySdk;
import io.opentelemetry.sdk.trace.samplers.Sampler;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Six acts against a real Jaeger, started and stopped by this program, and two real services
 * talking over real HTTP: the product page, in this program, and recommendations, in a second
 * Java program that this one starts.
 *
 * <p>A customer opens the page for product A-2231. The page looks the product up, prices it,
 * checks stock, asks recommendations what else to show, and renders. Every one of those steps
 * is a span. Everything the demo says about the trace, it reads back from Jaeger: nothing here
 * assembles a trace itself.
 */
public class JaegerTracingDemo {

    static final String SKU = "A-2231";
    static final int PAGE_SPANS = 6;
    static final int RECOMMENDATIONS_SPANS = 2;
    static final int SPANS_PER_PAGE = PAGE_SPANS + RECOMMENDATIONS_SPANS;
    static final long RECOMMENDATIONS_OWN_MILLIS = 60;
    static final long RANKING_MODEL_MILLIS = 340;
    static final int LOADS = 20;
    static final int KEEP_ONE_IN = 4;
    static final long CLOCK_OFF_MILLIS = -3000;

    public static void main(String[] args) {
        if (!JaegerServer.containerRuntimeAvailable()) {
            System.out.println(JaegerServer.NO_RUNTIME_ADVICE);
            return;
        }
        try (JaegerServer jaeger = new JaegerServer()) {
            try {
                jaeger.start();
            } catch (RuntimeException e) {
                System.out.println(JaegerServer.WOULD_NOT_START_ADVICE);
                return;
            }
            JaegerQuery held = jaeger.query();
            one(jaeger, held);
            two(jaeger, held);
            three(jaeger, held);
            four(jaeger, held);
            five(jaeger, held);
            six(jaeger, held);
        }
    }

    /** ONE. The page calls recommendations over HTTP, but does not write the header. */
    static void one(JaegerServer jaeger, JaegerQuery held) {
        System.out.println("ONE. A hop that forgets the header.");
        PageLoad load;
        try (Shop shop = Shop.normal(jaeger, 1, false)) {
            load = shop.load("visit-1");
            shop.stopPolitely();
        }
        Poll.until("both halves of visit-1 to reach Jaeger", () ->
                held.tracesForVisit(ProductPageService.NAME, "visit-1").size() == 1
                && held.tracesForVisit(RecommendationsService.NAME, "visit-1").size() == 1);
        HeldTrace pageTrace = awaitTrace(held, load.traceId(), PAGE_SPANS);
        HeldTrace recTrace = awaitTrace(held, load.recommendationsTraceId(), RECOMMENDATIONS_SPANS);
        long traces = pageTrace.traceId().equals(recTrace.traceId()) ? 1 : 2;
        HeldSpan call = pageTrace.named("call recommendations").orElseThrow();

        System.out.println("  the product page calls recommendations over real HTTP, in a second Java process.");
        System.out.println("  the page does not write the trace header onto that call. traceparent sent: " + load.sentHeader() + ".");
        System.out.println("  Jaeger holds " + traces + " traces for one page load, and neither says anything is wrong.");
        System.out.println("  trace " + shortId(pageTrace) + ": " + pageTrace.spans().size() + " spans, all from "
                + String.join(", ", servicesOf(pageTrace)) + ", " + pageTrace.roots() + " root.");
        System.out.println("    its call to recommendations has " + pageTrace.childrenOf(call).size() + " spans under it.");
        System.out.println("  trace " + shortId(recTrace) + ": " + recTrace.spans().size() + " spans, all from "
                + String.join(", ", servicesOf(recTrace)) + ", " + recTrace.roots() + " root.");
        System.out.println("    the ranking model is in here, with no page above it.");
        System.out.println("  the two were found together only by searching both services for the visit id the shop recorded.");
    }

    /** TWO. The same call, with the one line that writes the header. */
    static void two(JaegerServer jaeger, JaegerQuery held) {
        System.out.println("TWO. The header forwarded.");
        PageLoad load;
        try (Shop shop = Shop.normal(jaeger, 2, true)) {
            load = shop.load("visit-2");
            shop.stopPolitely();
        }
        HeldTrace trace = awaitTrace(held, load.traceId(), SPANS_PER_PAGE);
        System.out.println("  one line added: write the current trace context onto the outgoing request.");
        System.out.println("  traceparent sent:     " + load.sentHeader());
        System.out.println("  traceparent received: " + load.receivedHeader());
        System.out.println("  " + describeHeader(load.sentHeader()));
        System.out.println("  Jaeger holds " + (load.sentHeader().equals(load.receivedHeader()) ? 1 : 2) + " trace: "
                + trace.spans().size() + " spans from " + trace.servicesCount() + " services, " + trace.roots() + " root. its shape, as Jaeger holds it:");
        for (String line : tree(trace)) {
            System.out.println("    " + line);
        }
        HeldSpan slowest = slowestByOwnTime(trace);
        System.out.println("  the slowest piece of work, by its own time: " + slowest.name() + ", in " + slowest.service()
                + ", " + describeAtLeast(slowest, RANKING_MODEL_MILLIS) + ".");
        HeldSpan call = trace.named("call recommendations").orElseThrow();
        HeldSpan answer = trace.named("GET /recommendations").orElseThrow();
        System.out.println("  the page's call lasted " + (call.durationMicros() > answer.durationMicros() ? "longer" : "no longer")
                + " than recommendations took to answer. the difference is the hop itself.");
    }

    /** THREE. When the customer has the page, the collector does not have the trace yet. */
    static void three(JaegerServer jaeger, JaegerQuery held) {
        System.out.println("THREE. The collector puts it together, later.");
        try (Shop shop = Shop.normal(jaeger, 3, true)) {
            PageLoad load = shop.load("visit-3");
            long served = System.nanoTime();
            int atOnce = held.trace(load.traceId()).map(t -> t.spans().size()).orElse(0);
            System.out.println("  the customer has the page. Jaeger holds " + atOnce + " spans of it.");
            HeldTrace trace = awaitTrace(held, load.traceId(), SPANS_PER_PAGE);
            long lateMillis = (System.nanoTime() - served) / 1_000_000;
            System.out.println("  each service sends its finished spans by itself, in a batch every "
                    + Telemetry.BATCH_EVERY.toSeconds() + " seconds.");
            System.out.println("  the spans arrive " + describeLateness(lateMillis) + ".");
            System.out.println("  Jaeger then holds " + trace.spans().size() + " spans: " + trace.spansFrom(ProductPageService.NAME)
                    + " sent by product-page, " + trace.spansFrom(RecommendationsService.NAME)
                    + " sent by recommendations, joined by trace id.");
            shop.stopPolitely();
        }
    }

    /** FOUR. The front door keeps one trace in four, and the decision travels in the header. */
    static void four(JaegerServer jaeger, JaegerQuery held) {
        System.out.println("FOUR. Sampling at the front door.");
        List<PageLoad> loads = new ArrayList<>();
        Sampler oneInFour = Sampler.parentBased(Sampler.traceIdRatioBased(1.0 / KEEP_ONE_IN));
        try (Shop shop = new Shop(jaeger, 4, oneInFour, ProductPageService.Work.NONE, 0, 0, 0, true)) {
            for (int i = 1; i <= LOADS; i++) {
                loads.add(shop.load("visit-4-" + i));
            }
            shop.stopPolitely();
        }
        List<PageLoad> kept = loads.stream().filter(PageLoad::sampled).toList();
        List<PageLoad> dropped = loads.stream().filter(l -> !l.sampled()).toList();
        for (PageLoad k : kept) {
            awaitTrace(held, k.traceId(), SPANS_PER_PAGE);
        }
        long inJaeger = loads.stream().filter(l -> held.trace(l.traceId()).isPresent()).count();
        long recommendationsRecorded = kept.stream()
                .map(l -> held.trace(l.traceId()).orElseThrow())
                .filter(t -> t.spansFrom(RecommendationsService.NAME) > 0)
                .count();
        int complaint = loads.indexOf(dropped.get(0)) + 1;

        System.out.println("  the page keeps one trace in " + KEEP_ONE_IN + ", decided once, at the front door, from the trace id.");
        System.out.println("  " + LOADS + " page loads. kept: " + kept.size() + ". dropped: " + dropped.size() + ".");
        System.out.println("  a kept load's header ends -01:    " + kept.get(0).sentHeader());
        System.out.println("  a dropped load's header ends -00: " + dropped.get(0).sentHeader());
        System.out.println("  recommendations obeys the flag it is sent. it recorded spans for " + recommendationsRecorded + " page loads.");
        System.out.println("  Jaeger holds " + inJaeger + " traces of the " + LOADS + ".");
        System.out.println("  a customer complains about visit-4-" + complaint + ". Jaeger has "
                + (held.trace(dropped.get(0).traceId()).isPresent() ? "a" : "no") + " trace of it, and never will.");
    }

    /** FIVE. The recommendations machine's clock is three seconds slow. */
    static void five(JaegerServer jaeger, JaegerQuery held) {
        System.out.println("FIVE. A clock that is off.");
        PageLoad load;
        try (Shop shop = new Shop(jaeger, 5, Sampler.parentBased(Sampler.alwaysOn()), ProductPageService.Work.NORMAL,
                RECOMMENDATIONS_OWN_MILLIS, RANKING_MODEL_MILLIS, CLOCK_OFF_MILLIS, true)) {
            load = shop.load("visit-5");
            shop.stopPolitely();
        }
        HeldTrace trace = awaitTrace(held, load.traceId(), SPANS_PER_PAGE);
        HeldSpan call = trace.named("call recommendations").orElseThrow();
        HeldSpan answer = trace.named("GET /recommendations").orElseThrow();
        long earlyMillis = (call.startMicros() - answer.startMicros()) / 1000;
        boolean linksRight = trace.parentOf(answer).map(p -> p.spanId().equals(call.spanId())).orElse(false);

        System.out.println("  the recommendations machine's clock is " + Math.abs(CLOCK_OFF_MILLIS) / 1000 + " seconds slow. the page's clock is right.");
        System.out.println("  Jaeger holds 1 trace: " + trace.spans().size() + " spans, " + trace.roots() + " root. the parent links are "
                + (linksRight ? "all correct" : "broken") + ".");
        System.out.println("  in start order, Jaeger's first span is " + trace.inStartOrder().get(0).name()
                + ", before the page that asked for it.");
        System.out.println("  recommendations' span starts " + describeEarly(earlyMillis) + " before the call that caused it.");
        System.out.println("  Jaeger's own warning: " + describeWarning(trace.warnings()) + ".");
        System.out.println("  the collector stores what each service says. it does not correct a service's clock.");
    }

    /** SIX. The bill. */
    static void six(JaegerServer jaeger, JaegerQuery held) {
        System.out.println("SIX. The bill.");
        PageLoad load;
        try (Shop shop = Shop.normal(jaeger, 6, true)) {
            load = shop.load("visit-6");
            shop.recommendations.kill();
            shop.stopPolitely();
        }
        HeldTrace trace = awaitTrace(held, load.traceId(), PAGE_SPANS);
        HeldSpan call = trace.named("call recommendations").orElseThrow();
        System.out.println("  recommendations answers visit-6, then is killed before its next batch. the page stops politely.");
        System.out.println("  Jaeger holds " + trace.spans().size() + " spans of visit-6: " + trace.spansFrom(ProductPageService.NAME)
                + " from product-page, " + trace.spansFrom(RecommendationsService.NAME) + " from recommendations. they never arrive.");
        System.out.println("  the page's call to recommendations has " + trace.childrenOf(call).size()
                + " spans under it. the spans lost are the last ones before the crash.");
        System.out.println("  every page load costs " + SPANS_PER_PAGE + " spans from 2 processes, and a "
                + load.sentHeader().length() + " character traceparent header on every hop.");
        System.out.println("  and Jaeger is one more system to run. it said at start-up: " + jaeger.storageLine());
        System.out.println("  this demo needed 1 container for 2 service processes, and removes it, with every span in it, at the end.");
    }

    // ---------------------------------------------------------------------------------------
    // What the customer gets back, and the two services for one act.
    // ---------------------------------------------------------------------------------------

    /** What the customer's browser gets back, and what the page says about its own call. */
    record PageLoad(String traceId, boolean sampled, String sentHeader, String receivedHeader, String recommendationsTraceId) {

        static PageLoad from(String body) {
            Map<String, String> f = Http.fields(body);
            return new PageLoad(f.get("trace-id"), Boolean.parseBoolean(f.get("sampled")),
                    f.get("sent-traceparent"), f.get("received-traceparent"), f.get("recommendations-trace-id"));
        }
    }

    /**
     * The two services for one act, started fresh, so that every act's five-second batch timer
     * starts from zero and every act's ids start from the same seed on every run.
     */
    static final class Shop implements AutoCloseable {
        final OpenTelemetrySdk pageTelemetry;
        final RecommendationsProcess recommendations;
        final ProductPageService page;

        Shop(JaegerServer jaeger, long seed, Sampler sampler, ProductPageService.Work work,
             long recommendationsOwn, long ranking, long clockOffset, boolean forwardsTheHeader) {
            this.recommendations = RecommendationsProcess.start(jaeger.otlpEndpoint(), clockOffset,
                    recommendationsOwn, ranking, seed + 1000);
            this.pageTelemetry = Telemetry.start(
                    Telemetry.Settings.of(ProductPageService.NAME, jaeger.otlpEndpoint(), seed).keeping(sampler));
            this.page = new ProductPageService(pageTelemetry, recommendations.baseUrl(), work, forwardsTheHeader);
        }

        static Shop normal(JaegerServer jaeger, long seed, boolean forwardsTheHeader) {
            return new Shop(jaeger, seed, Sampler.parentBased(Sampler.alwaysOn()), ProductPageService.Work.NORMAL,
                    RECOMMENDATIONS_OWN_MILLIS, RANKING_MODEL_MILLIS, 0, forwardsTheHeader);
        }

        /** One customer opening the product page. */
        PageLoad load(String visit) {
            return PageLoad.from(Http.get(page.baseUrl() + "/product/" + SKU + "?visit=" + visit));
        }

        /** Both services shut down politely, which sends every span they still hold. */
        void stopPolitely() {
            recommendations.stop();
            page.close();
            Telemetry.stop(pageTelemetry);
        }

        @Override
        public void close() {
            recommendations.kill();
            page.close();
            Telemetry.stop(pageTelemetry);
        }
    }

    // ---------------------------------------------------------------------------------------
    // Reading the trace back, and describing in words what depends on timing.
    // ---------------------------------------------------------------------------------------

    /** Asks Jaeger, again and again, until it holds at least this many spans of the trace. */
    static HeldTrace awaitTrace(JaegerQuery held, String traceId, int spans) {
        Poll.until("Jaeger to hold " + spans + " spans of trace " + traceId,
                () -> held.trace(traceId).map(t -> t.spans().size() >= spans).orElse(false));
        return held.trace(traceId).orElseThrow();
    }

    /** The trace as an indented tree: a span's children sit under it, in the order they started. */
    static List<String> tree(HeldTrace trace) {
        List<String> lines = new ArrayList<>();
        for (HeldSpan span : trace.inStartOrder()) {
            if (span.isRoot()) {
                branch(trace, span, 0, lines);
            }
        }
        return lines;
    }

    private static void branch(HeldTrace trace, HeldSpan span, int depth, List<String> lines) {
        lines.add(String.format("%-26s %s", "  ".repeat(depth) + span.name(), span.service()));
        for (HeldSpan child : trace.childrenOf(span)) {
            branch(trace, child, depth + 1, lines);
        }
    }

    /** A span's own time: its length, less the time its children were running inside it. */
    static long ownMicros(HeldTrace trace, HeldSpan span) {
        return span.durationMicros() - trace.childrenOf(span).stream().mapToLong(HeldSpan::durationMicros).sum();
    }

    static HeldSpan slowestByOwnTime(HeldTrace trace) {
        HeldSpan slowest = trace.spans().get(0);
        for (HeldSpan span : trace.spans()) {
            if (ownMicros(trace, span) > ownMicros(trace, slowest)) {
                slowest = span;
            }
        }
        return slowest;
    }

    /**
     * Real durations wobble by a few milliseconds from run to run, so the demo says what is
     * certain rather than printing a number that would change.
     */
    static String describeAtLeast(HeldSpan span, long millis) {
        return span.durationMicros() >= millis * 1000 ? millis + " ms or more" : "under " + millis + " ms";
    }

    static String describeLateness(long millis) {
        if (millis > 2000) {
            return "more than 2 seconds after the customer had the page";
        }
        return "only " + millis + " ms after the customer had the page, sooner than usual";
    }

    static String describeEarly(long millis) {
        if (millis > 2000 && millis < 3000) {
            return "between 2 and 3 seconds";
        }
        return millis + " ms";
    }

    private static final Pattern DELTA = Pattern.compile("^(.*calculated delta of )([0-9.]+)s$");

    /**
     * Jaeger's warning ends with the exact amount it worked out, which wobbles with the real
     * durations. The words are printed as Jaeger wrote them; the amount is rounded to seconds.
     */
    static String describeWarning(List<String> warnings) {
        if (warnings.isEmpty()) {
            return "none";
        }
        Matcher m = DELTA.matcher(warnings.get(0));
        if (!m.matches()) {
            return warnings.get(0);
        }
        return m.group(1) + "about " + Math.round(Double.parseDouble(m.group(2))) + " seconds";
    }

    /** The header, field by field: version, trace id, the caller's span id, flags. */
    static String describeHeader(String header) {
        String[] parts = header.split("-");
        return "version " + parts[0] + ", trace id, the caller's span id, flags " + parts[3]
                + (parts[3].equals("01") ? ", which means sampled." : ", which means not sampled.");
    }

    static List<String> servicesOf(HeldTrace trace) {
        return trace.spans().stream().map(HeldSpan::service).distinct().sorted().toList();
    }

    static String shortId(HeldTrace trace) {
        return trace.traceId().substring(0, 8);
    }
}
