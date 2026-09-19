package com.jk.explore.circuitbreakerr4j;

import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

import java.util.List;

@SpringBootApplication
public class RecommendationsApplication {

    static SpringApplicationBuilder builder() {
        return new SpringApplicationBuilder(RecommendationsApplication.class).web(WebApplicationType.NONE);
    }

    static CircuitBreaker breaker(ConfigurableApplicationContext ctx, String name) {
        return ctx.getBean(CircuitBreakerRegistry.class).circuitBreaker(name);
    }

    public static void main(String[] args) {
        System.out.println("ONE. Healthy.");
        try (ConfigurableApplicationContext ctx = builder().run()) {
            RecommendationsClient client = ctx.getBean(RecommendationsClient.class);
            RecommendationsBackend backend = ctx.getBean(RecommendationsBackend.class);
            CircuitBreaker breaker = breaker(ctx, "recommendations");
            System.out.println("  page shows: " + client.fetch("MUG-BLUE") + ". breaker: " + breaker.getState() + ". backend calls: " + backend.calls() + ".");

            System.out.println("TWO. The service goes down.");
            backend.down(true);
            for (int i = 1; i <= 4; i++) {
                List<String> shown = client.fetch("MUG-BLUE");
                System.out.println("  call " + i + ": page shows " + shown + ". breaker: " + breaker.getState() + ". backend calls: " + backend.calls() + ".");
            }

            System.out.println("THREE. Open: fail fast.");
            int before = backend.calls();
            long refusedBefore = breaker.getMetrics().getNumberOfNotPermittedCalls();
            for (int i = 0; i < 100; i++) {
                client.fetch("MUG-BLUE");
            }
            System.out.println("  100 more page views. backend calls: " + (backend.calls() - before) + " more. breaker: " + breaker.getState() + ".");
            System.out.println("  calls refused by the breaker: " + (breaker.getMetrics().getNumberOfNotPermittedCalls() - refusedBefore) + ". the page never saw an error.");

            System.out.println("FOUR. Half-open: one probe.");
            breaker.transitionToHalfOpenState();
            int probeStart = backend.calls();
            client.fetch("MUG-BLUE");
            System.out.println("  service still down. one probe reached it (" + (backend.calls() - probeStart) + " call). breaker: " + breaker.getState() + ".");
            backend.down(false);
            breaker.transitionToHalfOpenState();
            System.out.println("  service back. the probe shows: " + client.fetch("MUG-BLUE") + ". breaker: " + breaker.getState() + ".");
        }

        System.out.println("FIVE. What counts as a failure.");
        try (ConfigurableApplicationContext ctx = builder().run()) {
            RecommendationsClient client = ctx.getBean(RecommendationsClient.class);
            for (int i = 0; i < 8; i++) {
                client.fetch("");
                client.fetchStrict("");
            }
            System.out.println("  8 requests for a product that does not exist.");
            System.out.println("  breaker that ignores IllegalArgumentException: " + breaker(ctx, "recommendations").getState() + ".");
            System.out.println("  breaker that counts everything: " + breaker(ctx, "strict").getState() + ".");
        }

        System.out.println("SIX. The annotation is a proxy.");
        try (ConfigurableApplicationContext ctx = builder().run()) {
            RecommendationsClient client = ctx.getBean(RecommendationsClient.class);
            RecommendationsBackend backend = ctx.getBean(RecommendationsBackend.class);
            backend.down(true);
            int errors = 0;
            for (int i = 0; i < 10; i++) {
                try {
                    client.fetchThroughThis("MUG-BLUE");
                } catch (BackendDown e) {
                    errors++;
                }
            }
            System.out.println("  10 calls through this. errors that reached the caller: " + errors + ". backend calls: " + backend.calls() + ".");
            System.out.println("  breaker: " + breaker(ctx, "recommendations").getState() + ". it never saw a call.");
        }
    }
}
