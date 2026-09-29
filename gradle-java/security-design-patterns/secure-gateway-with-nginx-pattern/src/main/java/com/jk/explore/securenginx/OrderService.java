package com.jk.explore.securenginx;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;

/**
 * The trusted order service, a real HTTP server on this machine. It holds the database password, and it
 * has internal features, an admin export and an admin header, that were never meant for the public.
 */
public final class OrderService implements AutoCloseable {

    static final String DATABASE_PASSWORD = "s3cret-db-password";

    private final HttpServer server;

    public OrderService() throws IOException {
        server = HttpServer.create(new InetSocketAddress("0.0.0.0", 0), 0);
        server.createContext("/", exchange -> {
            String path = exchange.getRequestURI().normalize().getPath();   // "/orders/../admin" becomes "/admin"
            exchange.getRequestBody().readAllBytes();
            String method = exchange.getRequestMethod();
            if ("true".equals(exchange.getRequestHeaders().getFirst("X-Internal-Admin")) || path.equals("/admin/export")) {
                reply(exchange, 200, "export of all 12000 orders");
            } else if (method.equals("GET") && path.startsWith("/orders/")) {
                reply(exchange, 200, "order " + path.substring("/orders/".length()));
            } else if (method.equals("POST") && path.equals("/orders")) {
                reply(exchange, 201, "order created");
            } else {
                reply(exchange, 404, "not found");
            }
        });
        server.start();
    }

    private static void reply(HttpExchange exchange, int status, String text) throws IOException {
        byte[] bytes = text.getBytes(StandardCharsets.UTF_8);
        exchange.sendResponseHeaders(status, bytes.length);
        try (OutputStream out = exchange.getResponseBody()) {
            out.write(bytes);
        }
    }

    public int port() {
        return server.getAddress().getPort();
    }

    public String url() {
        return "http://127.0.0.1:" + port();
    }

    @Override
    public void close() {
        server.stop(0);
    }
}
