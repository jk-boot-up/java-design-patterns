package com.jk.explore.valetkey;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

/**
 * The customer's browser, talking straight to storage with a key it was given.
 */
public final class Customer {

    private static final HttpClient HTTP = HttpClient.newHttpClient();

    public static String put(String url, byte[] body) throws Exception {
        HttpResponse<String> r = HTTP.send(HttpRequest.newBuilder(URI.create(url))
                .PUT(HttpRequest.BodyPublishers.ofByteArray(body)).build(), HttpResponse.BodyHandlers.ofString());
        return r.statusCode() + " " + r.body();
    }

    public static String get(String url) throws Exception {
        HttpResponse<String> r = HTTP.send(HttpRequest.newBuilder(URI.create(url)).build(),
                HttpResponse.BodyHandlers.ofString());
        return r.statusCode() + " " + r.body();
    }

    private Customer() {
    }
}
