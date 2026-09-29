package com.jk.explore.broker;

import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * The pattern: a go-between that knows where every service lives. Services register by name; clients call by name.
 *
 * <p>{@code /register?name=stock&url=...} adds an instance. {@code /call/stock?sku=...}
 * finds an instance of "stock" (taking turns between instances) and forwards the
 * request to it. Clients only ever know the broker's address.
 */
public final class Broker implements AutoCloseable {

    private final Map<String, List<String>> instances = new ConcurrentHashMap<>();
    private final Map<String, AtomicInteger> turn = new ConcurrentHashMap<>();
    private final AtomicInteger forwarded = new AtomicInteger();
    private final HttpServer server;

    public Broker() throws IOException {
        server = Http.serve("/", ex -> {
            String path = ex.getRequestURI().getPath();
            String query = ex.getRequestURI().getQuery();
            if (path.equals("/register")) {
                Map<String, String> p = params(query);
                register(p.get("name"), p.get("url"));
                Http.reply(ex, 200, "registered");
            } else if (path.startsWith("/call/")) {
                String name = path.substring("/call/".length());
                List<String> list = instances.getOrDefault(name, List.of());
                if (list.isEmpty()) {
                    Http.reply(ex, 404, "no service called " + name);
                    return;
                }
                String target = list.get(Math.floorMod(turn.computeIfAbsent(name, k -> new AtomicInteger()).getAndIncrement(), list.size()));
                forwarded.incrementAndGet();
                Http.reply(ex, 200, Http.get(target + "/?" + (query == null ? "" : query)));
            } else {
                Http.reply(ex, 404, "unknown");
            }
        });
    }

    /** A service announces itself; a moved service replaces its old address. */
    public synchronized void register(String name, String url) {
        instances.put(name, new ArrayList<>(List.of(url)));
    }

    /** A second instance of the same service. */
    public synchronized void addInstance(String name, String url) {
        instances.computeIfAbsent(name, k -> new ArrayList<>()).add(url);
    }

    private static Map<String, String> params(String q) {
        Map<String, String> p = new ConcurrentHashMap<>();
        for (String pair : q.split("&")) {
            String[] kv = pair.split("=", 2);
            p.put(kv[0], kv[1]);
        }
        return p;
    }

    public String url() {
        return Http.url(server);
    }

    public int forwarded() {
        return forwarded.get();
    }

    @Override
    public void close() {
        server.stop(0);
    }
}
