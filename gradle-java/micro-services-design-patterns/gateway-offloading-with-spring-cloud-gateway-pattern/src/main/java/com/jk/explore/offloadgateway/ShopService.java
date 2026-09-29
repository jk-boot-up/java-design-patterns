package com.jk.explore.offloadgateway;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.time.Instant;

/**
 * One of the shop's back-end services, a real HTTP server on a local port. It either checks the sign-in
 * token itself (the old way, possibly badly), or trusts the customer the gateway names in X-Customer.
 */
public final class ShopService implements AutoCloseable {

    public enum Mode { CHECKS_TOKEN, FORGETS_EXPIRY, TRUSTS_GATEWAY }

    private final HttpServer server;

    public ShopService(String name, Mode mode, String body) throws IOException {
        server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        server.createContext("/", exchange -> {
            String customer;
            if (mode == Mode.TRUSTS_GATEWAY) {
                customer = exchange.getRequestHeaders().getFirst("X-Customer");
            } else {
                String token = exchange.getRequestHeaders().getFirst("Authorization");
                customer = Tokens.customer(token);
                if (customer == null) {
                    reply(exchange, 401, "sign in");
                    return;
                }
                if (mode == Mode.CHECKS_TOKEN && Tokens.expired(token, Instant.now().getEpochSecond())) {
                    reply(exchange, 401, "token expired");
                    return;
                }
            }
            reply(exchange, 200, body.isEmpty() ? name + " for " + customer : body);
        });
        server.start();
    }

    private static void reply(HttpExchange exchange, int status, String text) throws IOException {
        byte[] bytes = text.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", text.startsWith("[") ? "application/json" : "text/plain");
        exchange.sendResponseHeaders(status, bytes.length);
        try (OutputStream out = exchange.getResponseBody()) {
            out.write(bytes);
        }
    }

    public String url() {
        return "http://127.0.0.1:" + server.getAddress().getPort();
    }

    @Override
    public void close() {
        server.stop(0);
    }
}
