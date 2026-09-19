package com.jk.explore.circuitbreakerr4j;

import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * The product page's view of the recommendations service. The breaker is an annotation: Spring
 * wraps this bean in a proxy, and Resilience4j counts every call that goes through it.
 */
@Service
public class RecommendationsClient {

    private final RecommendationsBackend backend;

    public RecommendationsClient(RecommendationsBackend backend) {
        this.backend = backend;
    }

    @CircuitBreaker(name = "recommendations", fallbackMethod = "none")
    public List<String> fetch(String sku) {
        return backend.recommendationsFor(sku);
    }

    /** The same call with a breaker that counts every exception, bad input included. */
    @CircuitBreaker(name = "strict", fallbackMethod = "none")
    public List<String> fetchStrict(String sku) {
        return backend.recommendationsFor(sku);
    }

    /** A call on this: it never meets the proxy, so it never meets the breaker. */
    public List<String> fetchThroughThis(String sku) {
        return withoutBreaker(sku);
    }

    @CircuitBreaker(name = "recommendations", fallbackMethod = "none")
    public List<String> withoutBreaker(String sku) {
        return backend.recommendationsFor(sku);
    }

    /** The product page renders without recommendations rather than failing. */
    List<String> none(String sku, Throwable cause) {
        return List.of();
    }
}
