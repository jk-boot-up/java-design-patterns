package com.jk.explore.microfrontends;

import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.Executors;
import java.util.function.Supplier;

/**
 * One team's own small web application, serving just its fragment of the page. Each runs, and is released, on its own.
 */
public final class TeamApp implements AutoCloseable {

    private final String team;
    private final HttpServer server;
    private volatile Supplier<String> fragment;
    private volatile int delayMs;

    public TeamApp(String team, Supplier<String> fragment) throws IOException {
        this.team = team;
        this.fragment = fragment;
        server = HttpServer.create(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0), 0);
        server.createContext("/fragment", ex -> {
            try {
                if (delayMs > 0) {
                    Thread.sleep(delayMs);
                }
                byte[] body = this.fragment.get().getBytes(StandardCharsets.UTF_8);
                ex.sendResponseHeaders(200, body.length);
                try (OutputStream out = ex.getResponseBody()) {
                    out.write(body);
                }
            } catch (InterruptedException | RuntimeException e) {
                ex.sendResponseHeaders(500, -1);
            }
        });
        server.setExecutor(Executors.newCachedThreadPool());
        server.start();
    }

    /** The team releases a new version of its fragment, without asking anyone. */
    public void release(Supplier<String> newFragment) {
        fragment = newFragment;
    }

    public void slowDown(int ms) {
        delayMs = ms;
    }

    public String url() {
        return "http://localhost:" + server.getAddress().getPort() + "/fragment";
    }

    public String team() {
        return team;
    }

    @Override
    public void close() {
        server.stop(0);
    }
}
