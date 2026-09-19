package com.jk.explore.pactcdc;

import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;

/** The catalog's price service, a real HTTP server: GET /prices/{sku}. */
public class Catalog implements AutoCloseable {

    private final HttpServer server;

    public Catalog(Release release) throws IOException {
        server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        server.createContext("/prices/", exchange -> {
            String sku = exchange.getRequestURI().getPath().substring("/prices/".length());
            byte[] body = release.body(sku).getBytes(StandardCharsets.UTF_8);
            exchange.getResponseHeaders().add("Content-Type", "application/json");
            exchange.sendResponseHeaders(200, body.length);
            exchange.getResponseBody().write(body);
            exchange.close();
        });
        server.start();
    }

    public int port() {
        return server.getAddress().getPort();
    }

    @Override
    public void close() {
        server.stop(0);
    }
}
