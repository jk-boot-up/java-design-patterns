package com.jk.explore.remotefacade;

import com.sun.net.httpserver.HttpExchange;
import java.io.IOException;
import java.io.OutputStream;
import java.net.URI;
import java.net.URLDecoder;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

/**
 * Helpers for the JDK web server, and a client that counts its round trips like a phone on a mobile network.
 */
public final class Http {

    /** A typical round trip for a phone on a mobile network. */
    public static final int MS_PER_TRIP = 80;

    public static Map<String, String> params(HttpExchange ex) {
        Map<String, String> p = new HashMap<>();
        String q = ex.getRequestURI().getRawQuery();
        if (q != null) {
            for (String pair : q.split("&")) {
                String[] kv = pair.split("=", 2);
                p.put(kv[0], URLDecoder.decode(kv.length > 1 ? kv[1] : "", StandardCharsets.UTF_8));
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

    public static String encode(String s) {
        return URLEncoder.encode(s, StandardCharsets.UTF_8);
    }

    /** The phone app's side: every call is one round trip over the network. */
    public static final class Phone {
        private final HttpClient client = HttpClient.newHttpClient();
        private final int port;
        private int trips;
        private long bytes;

        public Phone(int port) {
            this.port = port;
        }

        public String get(String path) {
            trips++;
            try {
                HttpResponse<String> r = client.send(
                        HttpRequest.newBuilder(URI.create("http://localhost:" + port + path)).build(),
                        HttpResponse.BodyHandlers.ofString());
                bytes += r.body().getBytes(StandardCharsets.UTF_8).length;
                return r.statusCode() == 200 ? r.body() : "ERROR " + r.body();
            } catch (IOException | InterruptedException e) {
                throw new IllegalStateException(e);
            }
        }

        public int trips() {
            return trips;
        }

        public long bytes() {
            return bytes;
        }

        public int waitedMs() {
            return trips * MS_PER_TRIP;
        }
    }

    private Http() {
    }
}
