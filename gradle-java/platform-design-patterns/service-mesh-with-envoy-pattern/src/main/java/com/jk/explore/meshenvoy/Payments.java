package com.jk.explore.meshenvoy;

import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.util.concurrent.atomic.AtomicInteger;

/** The payment service, a real HTTP server on this machine. On a bad day it refuses its first few calls. */
public class Payments implements AutoCloseable {

    private final HttpServer server;
    private final AtomicInteger received = new AtomicInteger();
    private volatile int refusals;

    public Payments() throws IOException {
        server = HttpServer.create(new InetSocketAddress("0.0.0.0", 0), 0);
        server.createContext("/", exchange -> {
            boolean ok = received.incrementAndGet() > refusals;
            byte[] body = (ok ? "charged" : "refused").getBytes();
            exchange.sendResponseHeaders(ok ? 200 : 503, body.length);
            exchange.getResponseBody().write(body);
            exchange.close();
        });
        server.start();
    }

    public int port() {
        return server.getAddress().getPort();
    }

    /** Starts a fresh bad day: the counter goes to zero, and the next few calls are refused. */
    public void badDay(int refusals) {
        this.refusals = refusals;
        received.set(0);
    }

    public int received() {
        return received.get();
    }

    @Override
    public void close() {
        server.stop(0);
    }
}
