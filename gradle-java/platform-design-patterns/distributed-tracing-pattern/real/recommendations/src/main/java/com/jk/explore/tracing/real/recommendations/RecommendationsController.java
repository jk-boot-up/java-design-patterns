package com.jk.explore.tracing.real.recommendations;

import io.micrometer.observation.Observation;
import io.micrometer.observation.ObservationRegistry;
import io.micrometer.tracing.Tracer;
import java.util.List;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * Tier 1's {@code recommendations} span, as a service with an HTTP door on it.
 *
 * <p>Tier 1 made the case that the ranking model is the expensive call and that
 * the only way to see it is to open a span around it and give that span a
 * parent. Here the parent arrives over the network, in a header this class never
 * reads.
 */
@RestController
public class RecommendationsController {

    /** Tier 1's scripted 340ms, kept as a constant so the two tiers agree. */
    private static final long RANKING_MODEL_MILLIS = 340;

    /** Tier 1's 60ms of self time -- the part recommendations does itself. */
    private static final long OWN_WORK_MILLIS = 60;

    private final ObservationRegistry registry;
    private final Tracer tracer;

    RecommendationsController(ObservationRegistry registry, Tracer tracer) {
        this.registry = registry;
        this.tracer = tracer;
    }

    @GetMapping("/recommendations")
    public Map<String, Object> recommend(
            @RequestParam String sku,
            // Read only so the demo can print it. Nothing in the propagation
            // depends on this parameter existing, and deleting it would change
            // no behaviour -- the server-side instrumentation has already taken
            // the header apart and opened a span before this method is entered.
            @RequestHeader(value = "traceparent", required = false) String traceparent) {

        pause(OWN_WORK_MILLIS);

        List<String> skus = Observation.createNotStarted("ranking-model", registry)
                .lowCardinalityKeyValue("model", "collaborative-v4")
                .observe(this::rank);

        return Map.of(
                "forSku", sku,
                "recommended", skus,
                // The whole of Tier 2's first claim, in one field. This is the
                // id the caller minted, seen from a different process.
                "traceId", tracer.currentSpan() == null
                        ? "none — this service is not in a trace"
                        : tracer.currentSpan().context().traceId(),
                "traceparentReceived", traceparent == null
                        ? "none — the caller sent no traceparent header"
                        : traceparent);
    }

    /**
     * The expensive call, wrapped in the one span this service opens for itself.
     *
     * <p>In Tier 1 this was {@code tracer.start(context, "ranking-model")} and
     * the context was passed by hand. The framework does the same thing here:
     * {@code observe} starts a span whose parent is whatever span is current on
     * this thread, which is the server span the incoming request opened.
     */
    private List<String> rank() {
        pause(RANKING_MODEL_MILLIS);
        return List.of("SKU-4417", "SKU-9002", "SKU-1183");
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
