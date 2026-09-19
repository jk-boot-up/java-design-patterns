package com.jk.explore.circuitbreakerr4j;

import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import org.junit.jupiter.api.Test;
import org.springframework.context.ConfigurableApplicationContext;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class BreakerTest {

    @Test
    void healthyCallsPassAndTheBreakerStaysClosed() {
        try (ConfigurableApplicationContext ctx = RecommendationsApplication.builder().run()) {
            assertEquals(2, ctx.getBean(RecommendationsClient.class).fetch("A").size());
            assertEquals(CircuitBreaker.State.CLOSED, RecommendationsApplication.breaker(ctx, "recommendations").getState());
        }
    }

    @Test
    void fourFailuresOpenTheBreakerAndTheFallbackKeepsThePageUp() {
        try (ConfigurableApplicationContext ctx = RecommendationsApplication.builder().run()) {
            ctx.getBean(RecommendationsBackend.class).down(true);
            RecommendationsClient client = ctx.getBean(RecommendationsClient.class);
            for (int i = 0; i < 4; i++) {
                assertEquals(List.of(), client.fetch("A"));
            }
            assertEquals(CircuitBreaker.State.OPEN, RecommendationsApplication.breaker(ctx, "recommendations").getState());
            assertEquals(4, ctx.getBean(RecommendationsBackend.class).calls());
        }
    }

    @Test
    void openBreakerRefusesWithoutTouchingTheBackend() {
        try (ConfigurableApplicationContext ctx = RecommendationsApplication.builder().run()) {
            RecommendationsBackend backend = ctx.getBean(RecommendationsBackend.class);
            backend.down(true);
            RecommendationsClient client = ctx.getBean(RecommendationsClient.class);
            for (int i = 0; i < 4; i++) client.fetch("A");
            for (int i = 0; i < 50; i++) client.fetch("A");
            assertEquals(4, backend.calls());
            assertEquals(50, RecommendationsApplication.breaker(ctx, "recommendations").getMetrics().getNumberOfNotPermittedCalls());
        }
    }

    @Test
    void halfOpenAllowsOneProbeAndClosesOnSuccess() {
        try (ConfigurableApplicationContext ctx = RecommendationsApplication.builder().run()) {
            RecommendationsBackend backend = ctx.getBean(RecommendationsBackend.class);
            RecommendationsClient client = ctx.getBean(RecommendationsClient.class);
            CircuitBreaker breaker = RecommendationsApplication.breaker(ctx, "recommendations");
            backend.down(true);
            for (int i = 0; i < 4; i++) client.fetch("A");
            breaker.transitionToHalfOpenState();
            client.fetch("A");
            assertEquals(CircuitBreaker.State.OPEN, breaker.getState());
            assertEquals(5, backend.calls());
            backend.down(false);
            breaker.transitionToHalfOpenState();
            assertEquals(2, client.fetch("A").size());
            assertEquals(CircuitBreaker.State.CLOSED, breaker.getState());
        }
    }

    @Test
    void ignoredExceptionsDoNotTripTheBreaker() {
        try (ConfigurableApplicationContext ctx = RecommendationsApplication.builder().run()) {
            RecommendationsClient client = ctx.getBean(RecommendationsClient.class);
            for (int i = 0; i < 8; i++) {
                client.fetch("");
                client.fetchStrict("");
            }
            assertEquals(CircuitBreaker.State.CLOSED, RecommendationsApplication.breaker(ctx, "recommendations").getState());
            assertEquals(CircuitBreaker.State.OPEN, RecommendationsApplication.breaker(ctx, "strict").getState());
        }
    }

    @Test
    void aCallOnThisBypassesTheBreakerAndTheFallback() {
        try (ConfigurableApplicationContext ctx = RecommendationsApplication.builder().run()) {
            ctx.getBean(RecommendationsBackend.class).down(true);
            RecommendationsClient client = ctx.getBean(RecommendationsClient.class);
            for (int i = 0; i < 10; i++) {
                assertThrows(BackendDown.class, () -> client.fetchThroughThis("A"));
            }
            assertEquals(CircuitBreaker.State.CLOSED, RecommendationsApplication.breaker(ctx, "recommendations").getState());
            assertEquals(10, ctx.getBean(RecommendationsBackend.class).calls());
        }
    }
}
