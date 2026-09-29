package com.jk.explore.valets3;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

/**
 * The customer's browser: it talks to the storage directly over HTTP, holding nothing but the key.
 */
public final class Browser {

    private final HttpClient http = HttpClient.newHttpClient();

    public int put(String url, byte[] data) throws Exception {
        return http.send(HttpRequest.newBuilder(URI.create(url)).PUT(HttpRequest.BodyPublishers.ofByteArray(data)).build(),
                HttpResponse.BodyHandlers.discarding()).statusCode();
    }

    public int get(String url) throws Exception {
        return http.send(HttpRequest.newBuilder(URI.create(url)).GET().build(),
                HttpResponse.BodyHandlers.discarding()).statusCode();
    }
}
