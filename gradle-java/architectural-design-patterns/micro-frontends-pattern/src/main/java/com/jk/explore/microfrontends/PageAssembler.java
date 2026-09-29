package com.jk.explore.microfrontends;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Collectors;

/**
 * The pattern: the page is a layout with slots; each slot is filled by fetching a fragment from the team that owns it.
 *
 * <p>Fragments are fetched at the same time. A fragment that fails or is too
 * slow is replaced by a fallback, so one team's problem does not take down the
 * page.
 */
public final class PageAssembler {

    private final HttpClient client = HttpClient.newBuilder().connectTimeout(Duration.ofMillis(300)).build();
    private final Map<String, String> slots = new LinkedHashMap<>();
    private int requests;

    public PageAssembler slot(String name, String url) {
        slots.put(name, url);
        return this;
    }

    public String render() {
        Map<String, CompletableFuture<String>> parts = new LinkedHashMap<>();
        slots.forEach((name, url) -> {
            requests++;
            HttpRequest req = HttpRequest.newBuilder(URI.create(url)).timeout(Duration.ofMillis(300)).build();
            parts.put(name, client.sendAsync(req, HttpResponse.BodyHandlers.ofString())
                    .thenApply(r -> r.statusCode() == 200 ? r.body() : fallback(name))
                    .exceptionally(e -> fallback(name)));
        });
        return parts.entrySet().stream().map(e -> "[" + e.getKey() + "] " + e.getValue().join())
                .collect(Collectors.joining(" | "));
    }

    private static String fallback(String name) {
        return "(" + name + " unavailable)";
    }

    public int requests() {
        return requests;
    }
}
