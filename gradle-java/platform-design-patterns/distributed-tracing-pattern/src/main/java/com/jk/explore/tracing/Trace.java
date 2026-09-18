package com.jk.explore.tracing;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * Every span from one customer's request, and the questions you can now answer.
 *
 * <p>The point of collecting spans into a trace is that a trace can be asked
 * things a log cannot. Which service took longest. What share of the page it
 * accounted for. Whether anything is missing. Those are the questions somebody
 * actually has at two in the morning, and they are all arithmetic once the
 * parent links are there.
 *
 * @param traceId the request these spans belong to
 * @param spans   the spans, in the order they were closed
 */
public record Trace(String traceId, List<Span> spans) {

    public Trace {
        spans = List.copyOf(spans);
    }

    /** The span at the front door, if this trace has one. */
    public Optional<Span> root() {
        return roots().stream().findFirst();
    }

    /**
     * Every span with no parent, earliest first.
     *
     * <p>A healthy trace has exactly one. More than one means the trace is
     * broken: some piece of work was started without being told what caused it,
     * so it floats free instead of hanging off the request. That is what a lost
     * context looks like from the outside, and it is why this returns a list
     * rather than an {@code Optional} — the plural case is not an edge case, it
     * is one of the three failures this project is about.
     */
    public List<Span> roots() {
        return spans.stream()
                .filter(Span::isRoot)
                // Ties on start time are broken by age, so that the span opened
                // first is drawn first. On a broken trace the genuine front door
                // and the orphaned work often start in the same millisecond, and
                // drawing the orphan above the request it escaped from reads
                // like nonsense.
                .sorted(Comparator.comparingLong(Span::startMillis)
                        .thenComparingInt(Trace::age))
                .toList();
    }

    /**
     * How early a span was opened, from the sequence in its id.
     *
     * <p>Leans on {@link Tracer} numbering ids {@code span-1}, {@code span-2} and
     * so on. A real tracer's ids are random and carry no order, which is why
     * this is a private detail of the drawing rather than part of {@link Span}.
     */
    private static int age(Span span) {
        int dash = span.spanId().lastIndexOf('-');
        try {
            return dash < 0 ? 0 : Integer.parseInt(span.spanId().substring(dash + 1));
        } catch (NumberFormatException notSequential) {
            return 0;
        }
    }

    /** When the last piece of work finished, across every root. */
    public long endMillis() {
        return spans.stream().mapToLong(Span::endMillis).max().orElse(0L);
    }

    /**
     * The direct children of a span, earliest first.
     *
     * <p>Sorting by start time is what makes the waterfall read left to right
     * the way the request actually happened.
     */
    public List<Span> childrenOf(String spanId) {
        return spans.stream()
                .filter(s -> spanId.equals(s.parentSpanId()))
                .sorted(Comparator.comparingLong(Span::startMillis))
                .toList();
    }

    /**
     * Spans whose parent is not in this trace.
     *
     * <p>These are the interesting ones, because an orphan is the signature of a
     * broken trace. A service that receives the context and forgets to pass it
     * on does not produce an error anywhere; it produces spans whose parent is a
     * span nobody has, or no spans at all. Either way the only symptom is that
     * the numbers stop adding up, which is why this method exists and why the
     * waterfall prints what it finds.
     */
    public List<Span> orphans() {
        Set<String> known = spans.stream().map(Span::spanId).collect(Collectors.toSet());
        return spans.stream()
                .filter(s -> !s.isRoot())
                .filter(s -> !known.contains(s.parentSpanId()))
                .sorted(Comparator.comparingLong(Span::startMillis))
                .toList();
    }

    /**
     * Time spent in each span excluding its children, by name, largest first.
     *
     * <p>Excluding children is the whole trick, and it is the difference between
     * a trace and a stopwatch. The root span lasted the entire request, so on
     * total time it is always the biggest and always useless. Subtract the work
     * it was waiting on and what is left is the time that service is actually
     * responsible for — which is the number that names the culprit.
     */
    public Map<String, Long> selfTimeByName() {
        List<Span> ranked = new ArrayList<>(spans);
        ranked.sort(Comparator.comparingLong(this::selfTime).reversed()
                .thenComparing(Span::name));

        Map<String, Long> byName = new LinkedHashMap<>();
        for (Span span : ranked) {
            byName.merge(span.name(), selfTime(span), Long::sum);
        }
        return byName;
    }

    /** This span's duration, less the time its children accounted for. */
    public long selfTime(Span span) {
        long childTime = childrenOf(span.spanId()).stream()
                .mapToLong(Span::durationMillis)
                .sum();
        return span.durationMillis() - childTime;
    }

    /** How long the whole request took, or zero if there is no root span. */
    public long totalMillis() {
        return root().map(Span::durationMillis).orElse(0L);
    }
}
