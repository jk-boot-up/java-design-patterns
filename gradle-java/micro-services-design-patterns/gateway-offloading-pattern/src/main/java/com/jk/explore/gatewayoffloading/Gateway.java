package com.jk.explore.gatewayoffloading;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.zip.GZIPOutputStream;

/**
 * The pattern: one gateway in front of every service does the shared chores once,
 * sign-in checks, rate limiting and compression, so the services do not have to.
 */
public final class Gateway {

    private final Map<String, Service> routes = new LinkedHashMap<>();
    private final Map<String, Integer> requestsThisSecond = new HashMap<>();
    private final int limitPerSecond;
    private long now;

    public Gateway(long now, int limitPerSecond) {
        this.now = now;
        this.limitPerSecond = limitPerSecond;
    }

    public Gateway route(String prefix, Service service) {
        routes.put(prefix, service);
        return this;
    }

    public void tick(long second) {
        now = second;
        requestsThisSecond.clear();
    }

    public Response handle(Request request) {
        // 1. sign-in, checked once, the same way for every service
        String token = request.header("Authorization");
        String customer = Tokens.customer(token);
        if (customer == null) {
            return Response.of(401, "sign in");
        }
        if (Tokens.expired(token, now)) {
            return Response.of(401, "token expired");
        }
        // 2. rate limit per customer
        int count = requestsThisSecond.merge(customer, 1, Integer::sum);
        if (count > limitPerSecond) {
            return Response.of(429, "too many requests");
        }
        // 3. route, passing on who the customer is
        Service target = routes.entrySet().stream()
                .filter(e -> request.path().startsWith(e.getKey()))
                .map(Map.Entry::getValue).findFirst().orElse(null);
        if (target == null) {
            return Response.of(404, "no such page");
        }
        Response response = target.handle(request.with("X-Customer", customer));
        // 4. compress for clients that accept it
        if ("gzip".equals(request.header("Accept-Encoding"))) {
            return new Response(response.status(), gzip(response.body()), true);
        }
        return response;
    }

    private static byte[] gzip(byte[] body) {
        ByteArrayOutputStream bytes = new ByteArrayOutputStream();
        try (GZIPOutputStream zip = new GZIPOutputStream(bytes)) {
            zip.write(body);
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
        return bytes.toByteArray();
    }
}
