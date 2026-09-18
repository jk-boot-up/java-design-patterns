package com.jk.explore.tracing;

import java.util.Map;

/**
 * The whole lesson, as one run.
 *
 * <p>Seven acts. The first two are the problem: a page that is too slow, and
 * four logs that cannot tell you why. The next two are the pattern: a trace id,
 * spans, and the waterfall that names the culprit in one line. The last three
 * are the bill — the three ways this goes wrong in practice, each of which costs
 * you the answer without telling you it has.
 *
 * <p>Everything printed here is computed, not typed. The percentages are
 * arithmetic on the spans; the waterfall is drawn from the parent links. Change
 * a duration in {@link ProductPage} and every number below moves with it, which
 * is the property that lets the documents and the video quote them.
 */
public final class ProductPageDemo {

    public static void main(String[] args) {
        heading("Act 1 — a product page takes nine hundred milliseconds");
        System.out.printf("""
                  A customer opens the page for product A-2231. It takes %dms.
                  Four services contributed to it: catalog, pricing, inventory
                  and recommendations. Nobody can say which one is at fault.
                %n""", ProductPage.PAGE_MS);

        heading("Act 2 — what the logs give you");
        System.out.println("""
                  Every service logs. The aggregator merges the four logs by
                  time. Two customers happen to be on the site at once.
                """);
        System.out.print(InterleavedLog.render(InterleavedLog.twoConcurrentPageLoads()));
        System.out.println("""
                  Read it and try to say how long pricing took.
                  There are two 'quote started' lines and two 'quote complete'
                  lines, and nothing says which belongs to which customer. The
                  timestamps are all correct and all useless. More logging does
                  not help: the missing thing is not detail, it is an identifier
                  that is the same across one request and different across the
                  next.
                """);

        heading("Act 3 — one id, and a parent for every piece of work");
        Trace trace = ProductPage.load("trace-4f2a");
        System.out.println("""
                  Now the front door mints a trace id and passes it down, and
                  every unit of work records a span: what it was, when it
                  started, how long it took, and what called it.
                """);
        for (Span span : trace.spans()) {
            System.out.printf("  %-16s %-10s parent %-10s %4dms%n",
                    span.name(), span.spanId(),
                    span.isRoot() ? "(none)" : span.parentSpanId(),
                    span.durationMillis());
        }

        heading("Act 4 — the waterfall, which is the answer");
        System.out.print(Waterfall.render(trace));
        System.out.println();
        reportCulprit(trace);

        heading("Act 5 — the bill, part one: one service is not instrumented");
        Trace partial = ProductPage.loadWithUninstrumentedRecommendations("trace-7c19");
        System.out.println("""
                  Recommendations is a well-behaved service in every respect but
                  one: it never opens a span. It still forwards the context, so
                  nothing errors and nothing warns.
                """);
        System.out.print(Waterfall.render(partial));
        System.out.printf("""
                %n  The time did not disappear. It landed on the parent.
                  The page now appears to spend %dms doing its own work, the
                  ranking model appears to hang directly off the page, and the
                  service actually responsible is not on the diagram at all.
                  Somebody spends the afternoon reading the page renderer.
                %n""", partial.selfTime(partial.root().orElseThrow()));

        heading("Act 6 — the bill, part two: the work moves to another thread");
        Trace broken = AsyncHandoff.withThreadLocalContext();
        System.out.println("""
                  The recommendations call is moved onto a worker thread so the
                  page can do other things meanwhile. The context lives in a
                  thread-local, which belongs to a thread and does not travel.
                """);
        System.out.print(Waterfall.render(broken));
        System.out.printf("""
                %n  Two roots in one trace, and %dms of work belonging to nobody.
                  The code that broke it is indistinguishable from the code that
                  worked. The fix is to capture the context as a value on the
                  calling thread and hand it to the task:
                %n""", ProductPage.RECOMMENDATIONS_MS);
        System.out.print(Waterfall.render(AsyncHandoff.withExplicitContext()));

        heading("Act 7 — the bill, part three: you kept one trace in a hundred");
        Sampler sampler = new Sampler(100);
        long requestsToday = 1_000_000;
        for (long i = 0; i < requestsToday; i++) {
            sampler.keep();
        }
        long complaint = 862_144;
        System.out.printf("""
                  A million requests today. Storing every span is not something
                  anybody pays for, so the front door keeps one trace in a
                  hundred.
                %n  kept       %,d
                  discarded  %,d
                %n  A customer complains about request number %,d.
                  Was it kept?  %s
                %n  It was decided at the front door, before anybody knew the
                  request was going to matter. That is the trade: a one per cent
                  sample answers 'recommendations is slow on average' perfectly
                  well, and cannot answer 'why was this one slow' at all.
                  The way out is tail sampling — hold the spans, decide to keep
                  the trace once you know it was slow.
                %n""",
                sampler.kept(), sampler.discarded(), complaint,
                sampler.wouldHaveKept(complaint) ? "yes" : "no — it is gone, and it is not recoverable");
    }

    /** Name the slowest piece of work, from the spans rather than from memory. */
    private static void reportCulprit(Trace trace) {
        Map<String, Long> selfTime = trace.selfTimeByName();
        String slowest = selfTime.keySet().iterator().next();
        long millis = selfTime.get(slowest);
        long total = trace.totalMillis();

        System.out.printf("""
                  Time by service, excluding what each was waiting on:
                %n""");
        selfTime.forEach((name, self) -> {
            if (self > 0) {
                System.out.printf("    %-16s %4dms   %2d%% of the page%n",
                        name, self, self * 100 / total);
            }
        });
        System.out.printf("""
                %n  The slowest single piece of work is %s, at %dms — %d%% of the
                  page. It sits inside recommendations, whose whole subtree is
                  %dms, or %d%% of what the customer waited for.
                %n  That is the question from Act 1, answered in one line of a
                  drawing, from data nobody had to guess at.
                %n""",
                slowest, millis, millis * 100 / total,
                ProductPage.RECOMMENDATIONS_MS,
                ProductPage.RECOMMENDATIONS_MS * 100 / total);
    }

    private static void heading(String title) {
        System.out.println();
        System.out.println("=".repeat(72));
        System.out.println("  " + title);
        System.out.println("=".repeat(72));
        System.out.println();
    }

    private ProductPageDemo() {
    }
}
