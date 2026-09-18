package com.jk.explore.tracing.real.recommendations;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * The downstream service, and the far end of the boundary the pattern is about.
 *
 * <p>There is no tracing code in this service at all beyond one
 * {@code observed} method. It does not read a header, it does not look for a
 * trace id, and it does not know that the caller has one. That is the point
 * worth carrying away from Tier 2: propagation is not something a service opts
 * into per call, it is something the framework does at both ends of every HTTP
 * hop, and a service's own code is left saying what it means rather than how
 * the context travels.
 */
@SpringBootApplication
public class RecommendationsApplication {

    public static void main(String[] args) {
        SpringApplication.run(RecommendationsApplication.class, args);
    }
}
