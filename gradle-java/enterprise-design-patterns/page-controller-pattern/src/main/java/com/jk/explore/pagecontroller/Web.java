package com.jk.explore.pagecontroller;

import com.sun.net.httpserver.HttpExchange;
import java.io.IOException;
import java.io.OutputStream;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

/**
 * Small helpers for the JDK's built-in web server: read the query string, send a reply, and make a request.
 */
public final class Web {

    public static Map<String, String> params(HttpExchange ex) {
        Map<String, String> p = new HashMap<>();
        String q = ex.getRequestURI().getQuery();
        if (q != null) {
            for (String pair : q.split("&")) {
                String[] kv = pair.split("=", 2);
                p.put(kv[0], kv.length > 1 ? kv[1] : "");
            }
        }
        return p;
    }

    public static void reply(HttpExchange ex, int status, String body) throws IOException {
        byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
        ex.sendResponseHeaders(status, bytes.length);
        try (OutputStream out = ex.getResponseBody()) {
            out.write(bytes);
        }
    }

    public static boolean loggedIn(HttpExchange ex) {
        String cookie = ex.getRequestHeaders().getFirst("Cookie");
        return cookie != null && cookie.contains("session=");
    }

    private static final HttpClient CLIENT = HttpClient.newHttpClient();

    /** GET a path on the local server; returns "status body". */
    public static String get(int port, String path, boolean withSession) {
        try {
            HttpRequest.Builder b = HttpRequest.newBuilder(URI.create("http://localhost:" + port + path));
            if (withSession) {
                b.header("Cookie", "session=priya");
            }
            HttpResponse<String> r = CLIENT.send(b.build(), HttpResponse.BodyHandlers.ofString());
            return r.statusCode() + " " + r.body();
        } catch (IOException | InterruptedException e) {
            throw new IllegalStateException(e);
        }
    }

    private Web() {
    }
}
