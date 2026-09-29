package com.jk.explore.securegateway;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Pattern;

/**
 * The pattern: the only machine the internet can reach. It holds no secrets and no data; it checks
 * every request against a short list of allowed shapes, strips anything internal, and only then
 * passes it to the trusted service.
 */
public final class Gatekeeper {

    record Route(String method, Pattern path) {
    }

    static final int MAX_BODY = 1_000_000;

    private final List<Route> allowed = List.of(
            new Route("GET", Pattern.compile("/orders/\\d{1,9}")),
            new Route("POST", Pattern.compile("/orders")));
    private final OrderService trusted;
    private int passed;
    private int refused;

    public Gatekeeper(OrderService trusted) {
        this.trusted = trusted;
    }

    public String handle(HttpRequest request) {
        if (request.bodyBytes() > MAX_BODY) {
            return refuse("413 too large");
        }
        boolean pathKnown = allowed.stream().anyMatch(r -> r.path().matcher(request.path()).matches());
        if (!pathKnown) {
            return refuse("404 not found");
        }
        boolean methodAllowed = allowed.stream()
                .anyMatch(r -> r.method().equals(request.method()) && r.path().matcher(request.path()).matches());
        if (!methodAllowed) {
            return refuse("405 method not allowed");
        }
        Map<String, String> clean = new HashMap<>(request.headers());
        clean.keySet().removeIf(h -> h.startsWith("X-Internal-"));
        passed++;
        return trusted.handle(new HttpRequest(request.method(), request.path(), clean, request.bodyBytes()));
    }

    /** The gatekeeper has no database password and no data of its own. */
    public boolean hasCredentials() {
        return false;
    }

    public int passed() {
        return passed;
    }

    public int refused() {
        return refused;
    }

    private String refuse(String status) {
        refused++;
        return status + " (stopped at the gate)";
    }
}
