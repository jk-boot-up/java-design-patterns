package com.jk.explore.stranglerfig.real;

import com.jk.explore.stranglerfig.domain.Line;
import com.jk.explore.stranglerfig.domain.Order;
import com.jk.explore.stranglerfig.domain.Pricer;
import com.jk.explore.stranglerfig.domain.Pricing;
import com.jk.explore.stranglerfig.fresh.NewPricing;
import com.jk.explore.stranglerfig.legacy.LegacyCheckout;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * <strong>Tier 1's classes, behind real HTTP.</strong> Run as {@code legacy} or as
 * {@code fresh}: the same {@code /api/orders/price?id=&subtotal=} endpoint, answered by
 * the legacy checkout's pricing or by the rewrite's. Nothing here is new logic, so
 * whatever the router does is done to the code Tier 1 already tested.
 */
public final class ServiceMain {

    public static void main(String[] args) throws IOException {
        String role = args[0];
        Pricer pricer = role.equals("legacy") ? new LegacyCheckout(Map.of()) : new NewPricing(false);
        AtomicInteger requests = new AtomicInteger();
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
        server.createContext("/api/orders/price", exchange -> {
            requests.incrementAndGet();
            Map<String, String> q = query(exchange.getRequestURI().getRawQuery());
            long subtotal = Long.parseLong(q.getOrDefault("subtotal", "0"));
            Pricing p = pricer.price(new Order(Integer.parseInt(q.getOrDefault("id", "0")), java.util.List.of(new Line("SKU-1", 1, subtotal))));
            String body = "total=" + p.totalPence() + " delivery=" + p.deliveryPence() + " servedBy=" + role + "\n";
            System.out.println("price id=" + q.get("id") + " -> " + body.trim());
            send(exchange, role, body);
        });
        server.createContext("/api/orders/stock", exchange -> {
            requests.incrementAndGet();
            send(exchange, role, "stock ok servedBy=" + role + "\n");
        });
        server.createContext("/stats", exchange -> send(exchange, role, "requests=" + requests.get() + " servedBy=" + role + "\n"));
        server.start();
        System.out.println(role + " listening on 8080");
    }

    private static void send(com.sun.net.httpserver.HttpExchange exchange, String role, String body) throws IOException {
        byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().add("X-Served-By", role);
        exchange.sendResponseHeaders(200, bytes.length);
        exchange.getResponseBody().write(bytes);
        exchange.close();
    }

    private static Map<String, String> query(String raw) {
        Map<String, String> out = new java.util.HashMap<>();
        if (raw != null) {
            for (String pair : raw.split("&")) {
                String[] kv = pair.split("=", 2);
                out.put(kv[0], kv.length > 1 ? kv[1] : "");
            }
        }
        return out;
    }
}
