package com.jk.explore.apigatewaysc;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * One of the shop's internal services, as a real HTTP server on a free port. It counts the
 * requests that reach it and remembers the last path and the last source header it saw.
 * Real sockets, real HTTP, no framework: the only Spring Cloud Gateway in the picture is the
 * one under test.
 */
public final class Backend implements AutoCloseable {

    private final String name;
    private final HttpServer server;
    private final AtomicInteger hits = new AtomicInteger();
    private volatile String lastPath = "";
    private volatile String lastSource = "";
    private volatile Gate slow;

    public Backend(String name) {
        this.name = name;
        try {
            server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        } catch (IOException e) {
            throw new IllegalStateException(e);
        }
        server.createContext("/", this::handle);
        server.start();
    }

    private void handle(HttpExchange exchange) throws IOException {
        hits.incrementAndGet();
        lastPath = exchange.getRequestURI().getPath();
        lastSource = String.valueOf(exchange.getRequestHeaders().getFirst("X-Request-Source"));
        Gate gate = slow;
        if (gate != null) {
            gate.arriveAndWait();
        }
        byte[] body = (name + " answers for " + lastPath).getBytes(StandardCharsets.UTF_8);
        exchange.sendResponseHeaders(200, body.length);
        exchange.getResponseBody().write(body);
        exchange.close();
    }

    public int port() {
        return server.getAddress().getPort();
    }

    public int hits() {
        return hits.get();
    }

    public String lastPath() {
        return lastPath;
    }

    public String lastSource() {
        return lastSource;
    }

    /** Every request from now on stops at the gate until it is opened. */
    public void slowDownAt(Gate gate) {
        this.slow = gate;
    }

    /** The service goes away: its port stays the same, and nothing is listening on it. */
    public void goDown() {
        server.stop(0);
    }

    @Override
    public void close() {
        server.stop(0);
    }
}
