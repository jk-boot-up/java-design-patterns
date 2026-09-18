package com.jk.explore.tracing.real.page;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestClient;

/**
 * Two HTTP clients to the same service, and the difference between them is the
 * whole of Tier 2's failure case.
 *
 * <p>Both send the same request to the same URL and both get the same answer
 * back. One of them puts the trace on the wire and one of them does not, and
 * nothing in either call site says which is which. That is why this is worth a
 * class of its own rather than a line inside the controller: the mistake is
 * invisible at the point where it is made, and the symptom appears in a tracing
 * tool somebody may not look at for a week.
 */
@Configuration
class RecommendationsClients {

    /**
     * The correct one.
     *
     * <p>The injected {@code RestClient.Builder} is the auto-configured one, and
     * Spring has already added an observation customiser to it. Every request
     * this client sends opens a client span and writes the current trace and
     * span id into a {@code traceparent} header. There is no tracing code here
     * because the instrumentation is on the builder, not on the call.
     */
    @Bean
    RestClient propagatingClient(RestClient.Builder builder) {
        return builder.baseUrl("http://localhost:8081").build();
    }

    /**
     * The broken one, and it is broken in the most ordinary way there is.
     *
     * <p>{@code RestClient.create()} is a static factory. It builds a client
     * from nothing, which means it never sees the customisers Spring would have
     * applied to the injected builder, which means no client span and no
     * {@code traceparent} header. It compiles, it passes its tests, it returns
     * the right recommendations, and it is one autocomplete away from the line
     * above it.
     *
     * <p>What it costs is Tier 1's Act 6 by a different route. The downstream
     * service starts a trace of its own, so the same customer request becomes
     * two traces that nothing connects — and neither of them looks broken on its
     * own. A team that only ever opens one trace at a time will not notice.
     */
    @Bean
    RestClient nonPropagatingClient() {
        return RestClient.create("http://localhost:8081");
    }
}
