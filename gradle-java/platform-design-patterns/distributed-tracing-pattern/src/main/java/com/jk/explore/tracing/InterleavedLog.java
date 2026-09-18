package com.jk.explore.tracing;

import java.util.Comparator;
import java.util.List;

/**
 * What you have before you have tracing: four logs, merged by time.
 *
 * <p>Every service writes a timestamped line when it starts and finishes. A log
 * aggregator collects them and shows them to you in time order. This is not a
 * strawman — it is what most teams actually have, and it is genuinely useful for
 * finding an error message.
 *
 * <p>It is useless for finding where time went, and the reason is worth saying
 * out loud because it is not obvious until you see it. The shop serves more than
 * one customer at a time. Two people open product pages a few milliseconds
 * apart, and now the merged log contains two pricing calls, two inventory calls
 * and two recommendation calls, interleaved. Nothing on any line says which
 * customer it belongs to. You cannot subtract one timestamp from another,
 * because you cannot tell whether the two lines are from the same request.
 *
 * <p>Adding more logging does not fix this. Only one thing fixes it: a value
 * that is the same on every line of one customer's request and different on
 * everybody else's. That value is the trace id, and once it is there the merged
 * log becomes readable again — which is the pattern, arrived at from the other
 * direction.
 */
public final class InterleavedLog {

    /**
     * One line in the merged log.
     *
     * @param atMillis when it was written, in milliseconds past the minute
     * @param service  which service wrote it
     * @param message  what it said
     */
    public record Line(long atMillis, String service, String message) {

        /** The line as a log aggregator would show it. */
        public String rendered() {
            return String.format("14:32:%02d.%03d  %-16s %s",
                    7 + atMillis / 1000, atMillis % 1000, service, message);
        }
    }

    private InterleavedLog() {
    }

    /**
     * Two customers opening product pages forty milliseconds apart.
     *
     * <p>Ada's request starts first. Ben's starts while hers is still running.
     * Both take the same route through the same four services, so the log below
     * contains two of everything, and no way to tell them apart.
     *
     * <p>The names are not in the log lines, deliberately. They are here in the
     * source so the test can check the interleaving is really happening; a real
     * log would not have them, which is the entire problem.
     */
    public static List<Line> twoConcurrentPageLoads() {
        List<Line> ada = oneRequest(0);
        List<Line> ben = oneRequest(40);

        return java.util.stream.Stream.concat(ada.stream(), ben.stream())
                .sorted(Comparator.comparingLong(Line::atMillis))
                .toList();
    }

    /**
     * The lines one page load produces, offset by when it started.
     *
     * <p>The durations are the same ones {@link ProductPage} uses, because it is
     * the same request seen two different ways.
     */
    private static List<Line> oneRequest(long startedAt) {
        long catalogDone = startedAt + ProductPage.CATALOG_MS;
        long pricingDone = catalogDone + ProductPage.PRICING_MS;
        long inventoryDone = pricingDone + ProductPage.INVENTORY_MS;
        long recsDone = inventoryDone + ProductPage.RECOMMENDATIONS_MS;
        long pageDone = recsDone + ProductPage.RENDER_MS;

        return List.of(
                new Line(startedAt, "gateway", "GET /product/A-2231"),
                new Line(startedAt, "catalog", "lookup started"),
                new Line(catalogDone, "catalog", "lookup complete"),
                new Line(catalogDone, "pricing", "quote started"),
                new Line(pricingDone, "pricing", "quote complete"),
                new Line(pricingDone, "inventory", "stock check started"),
                new Line(inventoryDone, "inventory", "stock check complete"),
                new Line(inventoryDone, "recommendations", "strip started"),
                new Line(recsDone, "recommendations", "strip complete"),
                new Line(pageDone, "gateway", "200 OK"));
    }

    /** The merged log, as the aggregator would print it. */
    public static String render(List<Line> lines) {
        StringBuilder out = new StringBuilder();
        for (Line line : lines) {
            out.append("  ").append(line.rendered()).append('\n');
        }
        return out.toString();
    }
}
