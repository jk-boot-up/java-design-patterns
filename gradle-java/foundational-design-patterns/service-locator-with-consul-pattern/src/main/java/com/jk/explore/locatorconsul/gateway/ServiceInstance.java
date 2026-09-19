package com.jk.explore.locatorconsul.gateway;

import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * <strong>A real HTTP service instance.</strong> It listens on a real port and
 * answers any request with its own identity, so a caller can tell which
 * instance served it. It stands for one running copy of the payment gateway, or
 * of the notifier.
 *
 * <p>It listens on every interface, not only loopback, because a Docker
 * container reaches the host through {@code host.docker.internal}. The port is
 * ephemeral, the instance answers only with an echo, and it lives for one run.
 */
public final class ServiceInstance implements AutoCloseable {

    private final String id;
    private final HttpServer server;
    private final AtomicInteger hits = new AtomicInteger();

    public ServiceInstance(String id) throws IOException {
        this.id = id;
        this.server = HttpServer.create(new InetSocketAddress(0), 0);
        this.server.createContext("/", exchange -> {
            hits.incrementAndGet();
            byte[] body = ("handled by " + id + ": " + exchange.getRequestURI().getQuery()).getBytes(StandardCharsets.UTF_8);
            exchange.sendResponseHeaders(200, body.length);
            exchange.getResponseBody().write(body);
            exchange.close();
        });
        this.server.start();
    }

    public String id() {
        return id;
    }

    public int port() {
        return server.getAddress().getPort();
    }

    public int hits() {
        return hits.get();
    }

    /** Stops listening. The instance is gone, whether or not anyone told Consul. */
    public void stop() {
        server.stop(0);
    }

    @Override
    public void close() {
        stop();
    }
}
