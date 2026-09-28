package com.jk.explore.stranglerfignginx;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * The small amount of plumbing both shop services share: start the JDK's built-in HTTP server,
 * and send a plain-text reply that names who sent it.
 */
final class ShopHttp {

    private ShopHttp() {
    }

    /**
     * Starts an HTTP server on the given port, or on any free port when the port is 0. Each
     * request gets its own thread, so one slow request never holds up another.
     */
    static HttpServer start(int port, ExecutorService threads) {
        try {
            HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
            server.setExecutor(threads);
            server.start();
            return server;
        } catch (IOException e) {
            throw new IllegalStateException("could not start an HTTP server on port " + port, e);
        }
    }

    static ExecutorService threads() {
        return Executors.newCachedThreadPool(r -> {
            Thread t = new Thread(r);
            t.setDaemon(true);
            return t;
        });
    }

    static void reply(HttpExchange exchange, int status, String servedBy, String text) throws IOException {
        byte[] body = text.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "text/plain; charset=utf-8");
        exchange.getResponseHeaders().set("X-Served-By", servedBy);
        exchange.sendResponseHeaders(status, body.length);
        try (OutputStream out = exchange.getResponseBody()) {
            out.write(body);
        }
    }

    /** The value of one cookie in the request, or null when the browser did not send it. */
    static String cookie(HttpExchange exchange, String name) {
        String header = exchange.getRequestHeaders().getFirst("Cookie");
        if (header == null) {
            return null;
        }
        for (String part : header.split(";")) {
            String[] pair = part.trim().split("=", 2);
            if (pair.length == 2 && pair[0].equals(name)) {
                return pair[1];
            }
        }
        return null;
    }

    static String query(HttpExchange exchange, String name) {
        String query = exchange.getRequestURI().getQuery();
        if (query == null) {
            return null;
        }
        for (String part : query.split("&")) {
            String[] pair = part.split("=", 2);
            if (pair.length == 2 && pair[0].equals(name)) {
                return pair[1];
            }
        }
        return null;
    }
}
