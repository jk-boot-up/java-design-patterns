package com.jk.explore.springcloudconfig;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

/** The few HTTP calls the demo makes, to the shop and to the config server. */
public final class Http {

    /** A status code and a body. */
    public record Reply(int status, String body) {
        public boolean ok() {
            return status >= 200 && status < 300;
        }
    }

    private static final HttpClient CLIENT = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(5))
            .build();

    private Http() {
    }

    public static Reply get(String url) {
        return send(HttpRequest.newBuilder(URI.create(url)).timeout(Duration.ofSeconds(30)).GET().build());
    }

    public static Reply post(String url) {
        return send(HttpRequest.newBuilder(URI.create(url)).timeout(Duration.ofSeconds(30))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.noBody()).build());
    }

    private static Reply send(HttpRequest request) {
        try {
            HttpResponse<String> r = CLIENT.send(request, HttpResponse.BodyHandlers.ofString());
            return new Reply(r.statusCode(), r.body());
        } catch (IOException e) {
            throw new IllegalStateException("no answer from " + request.uri(), e);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException("interrupted", e);
        }
    }

    /** A port nobody is listening on right now, for a process to take. */
    public static int freePort() {
        try (java.net.ServerSocket s = new java.net.ServerSocket(0)) {
            s.setReuseAddress(true);
            return s.getLocalPort();
        } catch (IOException e) {
            throw new IllegalStateException("no free port", e);
        }
    }
}
