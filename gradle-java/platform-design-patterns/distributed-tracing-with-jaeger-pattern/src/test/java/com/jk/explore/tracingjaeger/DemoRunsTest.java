package com.jk.explore.tracingjaeger;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;

/**
 * The demo is the document. Every figure quoted in the README, in the slides and in the
 * narration is asserted here, so a change that changes a figure fails the build instead of
 * quietly making the documents wrong.
 */
class DemoRunsTest {

    @Test
    void theSixActsRunAgainstARealJaegerAndPrintTheFiguresTheDocumentsQuote() {
        assumeTrue(JaegerServer.containerRuntimeAvailable(), "needs a container runtime");
        String out = runTheDemo();

        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        String[] expected = {
            "traceparent sent: none.",
            "Jaeger holds 2 traces for one page load, and neither says anything is wrong.",
            "trace beeb8da1: 6 spans, all from product-page, 1 root.",
            "its call to recommendations has 0 spans under it.",
            "trace 3ac55a49: 2 spans, all from recommendations, 1 root.",
            "traceparent sent:     00-bfc846100bfc1e42987bbcbfdd7e532f-b9f24f7bae4a6586-01",
            "traceparent received: 00-bfc846100bfc1e42987bbcbfdd7e532f-b9f24f7bae4a6586-01",
            "version 00, trace id, the caller's span id, flags 01, which means sampled.",
            "Jaeger holds 1 trace: 8 spans from 2 services, 1 root.",
            "        GET /recommendations   recommendations",
            "          ranking-model        recommendations",
            "the slowest piece of work, by its own time: ranking-model, in recommendations, 340 ms or more.",
            "the page's call lasted longer than recommendations took to answer.",
            "the customer has the page. Jaeger holds 0 spans of it.",
            "in a batch every 5 seconds.",
            "the spans arrive more than 2 seconds after the customer had the page.",
            "Jaeger then holds 8 spans: 6 sent by product-page, 2 sent by recommendations, joined by trace id.",
            "the page keeps one trace in 4, decided once, at the front door, from the trace id.",
            "20 page loads. kept: 6. dropped: 14.",
            "a kept load's header ends -01:    00-2ee9dc9fc86ae25de30fe2669284d85d-d6e5445f3c8658e2-01",
            "a dropped load's header ends -00: 00-e474c66a4b98b030dbef19fc8e7b845f-ebb1ae25f75e1f5e-00",
            "it recorded spans for 6 page loads.",
            "Jaeger holds 6 traces of the 20.",
            "a customer complains about visit-4-1. Jaeger has no trace of it, and never will.",
            "the recommendations machine's clock is 3 seconds slow.",
            "Jaeger holds 1 trace: 8 spans, 1 root. the parent links are all correct.",
            "in start order, Jaeger's first span is GET /recommendations, before the page that asked for it.",
            "recommendations' span starts between 2 and 3 seconds before the call that caused it.",
            "Jaeger's own warning: clock skew adjustment disabled; not applying calculated delta of about 3 seconds.",
            "Jaeger holds 6 spans of visit-6: 6 from product-page, 0 from recommendations. they never arrive.",
            "the page's call to recommendations has 0 spans under it.",
            "every page load costs 8 spans from 2 processes, and a 55 character traceparent header on every hop.",
            "using default All-in-One configuration with memory storage.",
            "1 container for 2 service processes",
        };
        for (String line : expected) {
            assertTrue(out.contains(line), "missing: " + line + "\n" + out);
        }
    }

    private static String runTheDemo() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            JaegerTracingDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }
}
