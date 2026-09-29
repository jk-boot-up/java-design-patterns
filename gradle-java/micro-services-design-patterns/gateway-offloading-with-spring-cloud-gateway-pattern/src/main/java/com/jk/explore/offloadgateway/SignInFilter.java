package com.jk.explore.offloadgateway;

import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.cloud.gateway.filter.GlobalFilter;
import org.springframework.core.Ordered;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

/**
 * The chores the gateway does for every service, before any route: check the sign-in token, limit each
 * customer's requests, and pass on who the customer is, removing any X-Customer the caller sent.
 */
@Component
public class SignInFilter implements GlobalFilter, Ordered {

    static final int PER_MINUTE = 5;

    /** A token bucket per customer: holds 5, refills 5 a minute. Production uses the built-in
     *  RequestRateLimiter filter with Redis, so every gateway instance shares the count. */
    private final Map<String, double[]> buckets = new ConcurrentHashMap<>();

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        String token = exchange.getRequest().getHeaders().getFirst("Authorization");
        String customer = Tokens.customer(token);
        if (customer == null) {
            return refuse(exchange, HttpStatus.UNAUTHORIZED, "sign in");
        }
        if (Tokens.expired(token, Instant.now().getEpochSecond())) {
            return refuse(exchange, HttpStatus.UNAUTHORIZED, "token expired");
        }
        if (!take(customer)) {
            return refuse(exchange, HttpStatus.TOO_MANY_REQUESTS, "too many requests");
        }
        ServerWebExchange passOn = exchange.mutate().request(r -> r.headers(h -> {
            h.remove("X-Customer");            // a caller cannot claim to be someone else
            h.add("X-Customer", customer);
        })).build();
        return chain.filter(passOn);
    }

    private static Mono<Void> refuse(ServerWebExchange exchange, HttpStatus status, String why) {
        exchange.getResponse().setStatusCode(status);
        return exchange.getResponse().writeWith(Mono.just(
                exchange.getResponse().bufferFactory().wrap(why.getBytes(StandardCharsets.UTF_8))));
    }

    /** Takes one token from the customer's bucket, refilling it for the time that has passed. */
    private boolean take(String customer) {
        long nowMillis = System.currentTimeMillis();
        double[] bucket = buckets.computeIfAbsent(customer, k -> new double[] {PER_MINUTE, nowMillis});
        synchronized (bucket) {
            bucket[0] = Math.min(PER_MINUTE, bucket[0] + (nowMillis - bucket[1]) * PER_MINUTE / 60_000.0);
            bucket[1] = nowMillis;
            if (bucket[0] < 1) {
                return false;
            }
            bucket[0]--;
            return true;
        }
    }

    public void reset() {
        buckets.clear();
    }

    @Override
    public int getOrder() {
        return -100;
    }
}
