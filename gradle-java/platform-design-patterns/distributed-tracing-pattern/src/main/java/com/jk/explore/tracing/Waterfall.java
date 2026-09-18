package com.jk.explore.tracing;

/**
 * The trace, drawn.
 *
 * <p>This class is the payoff of the whole project, and it is worth being clear
 * about what it is. A hosted tracing tool shows you a page of horizontal bars,
 * one per span, nested and laid out on a shared timeline. That picture is not a
 * feature of the tool — it is simply what a set of spans <em>looks like</em> once
 * each one knows its parent. Drawing it in the console is therefore not a
 * substitute for real tracing. It is the thing real tracing exists to produce.
 *
 * <p>For a listener rather than a viewer: each line is one unit of work. The
 * name is on the left, indented under whatever called it. The bar to its right
 * starts where that work started and its length is how long it took, all drawn
 * against the same timeline, so the page's nine hundred milliseconds spans the
 * full width and everything else is a fraction of it. A short bar far to the
 * right is work that happened late and quickly; a long bar is where your time
 * went.
 */
public final class Waterfall {

    /** Characters of bar used for the full width of the request. */
    private static final int BAR = 44;

    private static final int NAME_COLUMN = 24;

    private Waterfall() {
    }

    /**
     * Render the trace as an indented timeline.
     *
     * @return the drawing, with a trailing newline on every line, or an
     *         explanation if the trace has no root span to scale against
     */
    public static String render(Trace trace) {
        StringBuilder out = new StringBuilder();

        var roots = trace.roots();
        if (roots.isEmpty()) {
            return "  no root span — this trace has no front door, so there is "
                    + "nothing to measure the parts against.\n";
        }

        // Scaled against the whole elapsed time rather than against the first
        // root's duration. On a healthy trace those are the same number. On a
        // broken one they are not, and scaling to the first root would draw the
        // orphaned work as though it filled the request — which would hide the
        // very thing this drawing is being used to show.
        long total = Math.max(trace.endMillis(), 1);

        out.append("  trace ").append(trace.traceId())
                .append("   total ").append(total).append("ms");
        if (roots.size() > 1) {
            out.append("   ").append(roots.size())
                    .append(" separate roots — this trace is broken");
        }
        out.append('\n');

        for (Span root : roots) {
            appendSpan(out, trace, root, 0, total);
        }

        var orphans = trace.orphans();
        if (!orphans.isEmpty()) {
            out.append("\n  ").append(orphans.size())
                    .append(orphans.size() == 1 ? " span whose parent is missing"
                            : " spans whose parent is missing")
                    .append(" — the trace is broken above these:\n");
            for (Span orphan : orphans) {
                appendSpan(out, trace, orphan, 1, total);
            }
        }
        return out.toString();
    }

    private static void appendSpan(StringBuilder out, Trace trace, Span span,
                                   int depth, long total) {

        String label = "  ".repeat(depth) + span.name();
        out.append("  ").append(pad(label, NAME_COLUMN));

        // Where the bar starts, and how long it is, both as a share of the
        // whole request. A span shorter than one character of bar is still
        // drawn as one character, because a span that rounded away to nothing
        // would look like a span that never happened.
        int offset = (int) (span.startMillis() * BAR / total);
        int length = Math.max(1, (int) (span.durationMillis() * BAR / total));
        if (offset + length > BAR) {
            length = Math.max(1, BAR - offset);
        }

        out.append('|')
                .append(" ".repeat(offset))
                .append("=".repeat(length))
                .append(" ".repeat(Math.max(0, BAR - offset - length)))
                .append('|');

        out.append(String.format("%6dms", span.durationMillis()));

        long self = trace.selfTime(span);
        if (self != span.durationMillis()) {
            out.append(String.format("   %dms of it its own", self));
        }
        out.append('\n');

        for (Span child : trace.childrenOf(span.spanId())) {
            appendSpan(out, trace, child, depth + 1, total);
        }
    }

    private static String pad(String text, int width) {
        return text.length() >= width ? text : text + " ".repeat(width - text.length());
    }
}
