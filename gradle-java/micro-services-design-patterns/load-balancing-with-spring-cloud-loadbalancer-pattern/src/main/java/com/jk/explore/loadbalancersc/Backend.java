package com.jk.explore.loadbalancersc;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * One copy of the catalogue service, as a real HTTP server on a free port. It counts the
 * requests it answers. {@code cost} is how much work one request is on this copy: the
 * older machine costs six times as much, and the demo adds costs up instead of timing them.
 */
public final class Backend implements AutoCloseable {

    private final String name;
    private final int cost;
    private final HttpServer server;
    private final AtomicInteger hits = new AtomicInteger();

    public Backend(String name, int cost) {
        this.name = name;
        this.cost = cost;
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
        byte[] body = name.getBytes(StandardCharsets.UTF_8);
        exchange.sendResponseHeaders(200, body.length);
        exchange.getResponseBody().write(body);
        exchange.close();
    }

    public String name() {
        return name;
    }

    public int port() {
        return server.getAddress().getPort();
    }

    public int cost() {
        return cost;
    }

    public int hits() {
        return hits.get();
    }

    public int work() {
        return hits.get() * cost;
    }

    public void goDown() {
        server.stop(0);
    }

    @Override
    public void close() {
        server.stop(0);
    }
}
