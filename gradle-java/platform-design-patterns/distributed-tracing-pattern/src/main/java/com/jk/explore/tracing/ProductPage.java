package com.jk.explore.tracing;

/**
 * The product page, and the four services that build it.
 *
 * <p>A customer opens a product page. Behind that one request the shop asks the
 * catalog for the product, pricing for the price, inventory for the stock
 * figure, and recommendations for the "customers also bought" strip, and then
 * renders the page. Five pieces of work, nine hundred milliseconds, and the
 * question the whole project exists to answer: <em>which of them is the slow
 * one?</em>
 *
 * <p>The durations below are declared rather than measured, so that every number
 * in the tests, the documents and the video is the same on every run. See
 * {@link Clock} for why.
 */
public final class ProductPage {

    /** Looking the product up. Fast, and not the problem. */
    public static final long CATALOG_MS = 120;

    /** Working out the price for this customer. */
    public static final long PRICING_MS = 180;

    /** Asking the warehouse how many are left. */
    public static final long INVENTORY_MS = 90;

    /** The "customers also bought" strip. This is the slow one. */
    public static final long RECOMMENDATIONS_MS = 400;

    /** Inside recommendations: scoring the candidates. Slower still. */
    public static final long RANKING_MODEL_MS = 340;

    /** Turning it all into HTML. */
    public static final long RENDER_MS = 110;

    /** What the customer experiences, and the sum of everything above. */
    public static final long PAGE_MS =
            CATALOG_MS + PRICING_MS + INVENTORY_MS + RECOMMENDATIONS_MS + RENDER_MS;

    private ProductPage() {
    }

    /**
     * One page load with every service instrumented.
     *
     * <p>Read the shape of this method rather than its contents. Every unit of
     * work opens a span, passes {@code scope.context()} to anything it calls,
     * and closes the span when it is done. That is all the pattern asks. The
     * waterfall, the self times and the answer to "which service" all fall out
     * of those three habits.
     */
    public static Trace load(String traceId) {
        Clock.Scripted clock = new Clock.Scripted();
        Tracer tracer = new Tracer(traceId, clock);

        try (Tracer.Scope page = tracer.startRoot("product-page")) {
            TraceContext request = page.context();

            try (Tracer.Scope catalog = tracer.start(request, "catalog")) {
                clock.advance(CATALOG_MS);
            }
            try (Tracer.Scope pricing = tracer.start(request, "pricing")) {
                clock.advance(PRICING_MS);
            }
            try (Tracer.Scope inventory = tracer.start(request, "inventory")) {
                clock.advance(INVENTORY_MS);
            }

            // Recommendations does some work of its own and then calls a
            // scoring model. The nesting is the reason a trace beats a
            // stopwatch: it can tell you not just which service was slow but
            // which part of it.
            try (Tracer.Scope recommendations = tracer.start(request, "recommendations")) {
                try (Tracer.Scope model =
                             tracer.start(recommendations.context(), "ranking-model")) {
                    clock.advance(RANKING_MODEL_MS);
                }
                clock.advance(RECOMMENDATIONS_MS - RANKING_MODEL_MS);
            }

            try (Tracer.Scope render = tracer.start(request, "render")) {
                clock.advance(RENDER_MS);
            }
        }
        return tracer.trace();
    }

    /**
     * The same page load, with recommendations not instrumented.
     *
     * <p>This is the first item on the bill, and it does not fail the way people
     * expect. Recommendations here is a well-behaved service in every respect
     * except one: it never opens a span of its own. It still receives the
     * context and still passes it on faithfully, so nothing errors, nothing
     * warns, and the trace still looks complete.
     *
     * <p>What happens instead is that the four hundred milliseconds does not
     * disappear — it has to land somewhere, and it lands on the parent. The page
     * span suddenly appears to be doing sixty milliseconds of work by itself,
     * the ranking model appears to hang directly off the page, and the service
     * that is actually responsible is not on the diagram at all. Somebody then
     * spends an afternoon looking at the page renderer.
     *
     * <p>That is the real cost of partial instrumentation: not a gap you can
     * see, but a wrong answer you cannot.
     */
    public static Trace loadWithUninstrumentedRecommendations(String traceId) {
        Clock.Scripted clock = new Clock.Scripted();
        Tracer tracer = new Tracer(traceId, clock);

        try (Tracer.Scope page = tracer.startRoot("product-page")) {
            TraceContext request = page.context();

            try (Tracer.Scope catalog = tracer.start(request, "catalog")) {
                clock.advance(CATALOG_MS);
            }
            try (Tracer.Scope pricing = tracer.start(request, "pricing")) {
                clock.advance(PRICING_MS);
            }
            try (Tracer.Scope inventory = tracer.start(request, "inventory")) {
                clock.advance(INVENTORY_MS);
            }

            // No span opened here. The context is forwarded unchanged, which is
            // the part that makes this so hard to spot: the chain is not
            // broken, it is just missing a link, so the model's parent becomes
            // the page.
            try (Tracer.Scope model = tracer.start(request, "ranking-model")) {
                clock.advance(RANKING_MODEL_MS);
            }
            clock.advance(RECOMMENDATIONS_MS - RANKING_MODEL_MS);

            try (Tracer.Scope render = tracer.start(request, "render")) {
                clock.advance(RENDER_MS);
            }
        }
        return tracer.trace();
    }
}
