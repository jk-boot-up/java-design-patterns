package com.jk.explore.tracing.real.page;

import io.micrometer.observation.Observation;
import io.micrometer.observation.ObservationRegistry;
import io.micrometer.tracing.Tracer;
import java.util.LinkedHashMap;
import java.util.Map;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestClient;

/**
 * Tier 1's {@code ProductPage}, rendering the same page across a real network
 * hop.
 *
 * <p>The page does three things: a catalog lookup, a pricing call and a
 * recommendations call. The first two are local and are wrapped in observations
 * so that they appear as spans, exactly as Tier 1 wrapped them. The third leaves
 * the process, and which client it leaves by is the only interesting decision in
 * this class.
 */
@RestController
class ProductPageController {

    /** Tier 1's scripted figures, so the two tiers can be read side by side. */
    private static final long CATALOG_MILLIS = 120;
    private static final long PRICING_MILLIS = 180;

    private final ObservationRegistry registry;
    private final Tracer tracer;
    private final RestClient propagating;
    private final RestClient nonPropagating;

    ProductPageController(ObservationRegistry registry,
                          Tracer tracer,
                          @Qualifier("propagatingClient") RestClient propagating,
                          @Qualifier("nonPropagatingClient") RestClient nonPropagating) {
        this.registry = registry;
        this.tracer = tracer;
        this.propagating = propagating;
        this.nonPropagating = nonPropagating;
    }

    /**
     * @param propagate when false, calls recommendations with the client that
     *                  forgets to forward the context. The page renders
     *                  identically either way, which is the point being made.
     */
    @GetMapping("/page")
    public Map<String, Object> page(@RequestParam(defaultValue = "SKU-4417") String sku,
                                    @RequestParam(defaultValue = "true") boolean propagate) {

        String pageTraceId = tracer.currentSpan() == null
                ? "none"
                : tracer.currentSpan().context().traceId();

        Observation.createNotStarted("catalog", registry).observe(() -> pause(CATALOG_MILLIS));
        Observation.createNotStarted("pricing", registry).observe(() -> pause(PRICING_MILLIS));

        RestClient client = propagate ? propagating : nonPropagating;
        @SuppressWarnings("unchecked")
        Map<String, Object> downstream = client.get()
                .uri("/recommendations?sku={sku}", sku)
                .retrieve()
                .body(Map.class);

        // Assembled in order rather than with Map.of, because the demo prints
        // this and the two trace ids have to sit next to each other to be
        // compared at a glance.
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("sku", sku);
        out.put("propagated", propagate);
        out.put("pageTraceId", pageTraceId);
        out.put("recommendationsTraceId", downstream.get("traceId"));
        out.put("traceparentSeenDownstream", downstream.get("traceparentReceived"));
        out.put("sameTrace", pageTraceId.equals(downstream.get("traceId")));
        out.put("recommended", downstream.get("recommended"));
        return out;
    }

    private static void pause(long millis) {
        try {
            Thread.sleep(millis);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
    }
}
