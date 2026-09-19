package com.jk.explore.bgk8s;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.Map;
import java.util.TreeMap;
import java.util.function.BooleanSupplier;

/** Sends requests to the service through the port kind maps to this machine. */
public class Traffic {

    public record Outcome(Map<String, Integer> answers, int failed) {
        public int from(String version) {
            return answers.getOrDefault(version, 0);
        }
    }

    private final int port;

    public Traffic(int port) {
        this.port = port;
    }

    /** One request. Returns the body if it was answered with 200, and null if it failed in any way. */
    public String get(String path) {
        // A new client for every request, so that no connection is reused: a kept-alive connection
        // would stay on the pod it first reached, and hide both the switch and the spread of a canary.
        try (HttpClient client = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(2)).build()) {
            HttpResponse<String> r = client.send(HttpRequest.newBuilder(URI.create("http://127.0.0.1:" + port + path))
                    .timeout(Duration.ofSeconds(3)).build(), HttpResponse.BodyHandlers.ofString());
            return r.statusCode() == 200 ? r.body() : null;
        } catch (Exception e) {
            return null;
        }
    }

    public Outcome send(String path, int n) {
        Map<String, Integer> answers = new TreeMap<>();
        int failed = 0;
        for (int i = 0; i < n; i++) {
            String body = get(path);
            if (body == null) {
                failed++;
            } else {
                answers.merge(body, 1, Integer::sum);
            }
        }
        return new Outcome(answers, failed);
    }

    /** Waits, for a bounded time, until a probe says the switch has reached the cluster's rules. */
    public static void waitUntil(BooleanSupplier condition) {
        long end = System.nanoTime() + Duration.ofSeconds(60).toNanos();
        while (System.nanoTime() < end) {
            if (condition.getAsBoolean()) {
                return;
            }
            try {
                Thread.sleep(200);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
        }
        throw new IllegalStateException("the cluster did not settle in 60 seconds");
    }
}
