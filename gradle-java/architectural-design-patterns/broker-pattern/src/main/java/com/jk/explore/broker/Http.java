package com.jk.explore.broker;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.Executors;

/**
 * Small helpers: start a local web server, reply to a request, and make a GET request.
 */
public final class Http {

    private static final HttpClient CLIENT = HttpClient.newHttpClient();

    public static HttpServer serve(String path, HttpHandler handler) throws IOException {
        HttpServer s = HttpServer.create(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0), 0);
        s.createContext(path, handler);
        s.setExecutor(Executors.newCachedThreadPool());
        s.start();
        return s;
    }

    public static String url(HttpServer s) {
        return "http://localhost:" + s.getAddress().getPort();
    }

    public static void reply(HttpExchange ex, int status, String body) throws IOException {
        byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
        ex.sendResponseHeaders(status, bytes.length);
        try (OutputStream out = ex.getResponseBody()) {
            out.write(bytes);
        }
    }

    /** GET a URL; returns the body, or "FAILED, ..." if nothing answers. */
    public static String get(String url) {
        try {
            HttpResponse<String> r = CLIENT.send(HttpRequest.newBuilder(URI.create(url)).build(),
                    HttpResponse.BodyHandlers.ofString());
            return r.statusCode() == 200 ? r.body() : "FAILED, " + r.body();
        } catch (IOException e) {
            return "FAILED, " + (e.getMessage() == null ? "connection refused" : "connection refused");
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return "FAILED, interrupted";
        }
    }

    private Http() {
    }
}
