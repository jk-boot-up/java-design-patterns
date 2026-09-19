package com.jk.explore.meshenvoy;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

/** A service that calls payments over HTTP. It can carry its own retry code, or none at all. */
public class Caller {

    private final String name;
    private final int retries;

    public Caller(String name, int retries) {
        this.name = name;
        this.retries = retries;
    }

    public String name() {
        return name;
    }

    /** True if payments, or the proxy in front of it, answered with 200. */
    public boolean call(String url) {
        for (int attempt = 0; attempt <= retries; attempt++) {
            if (status(url) == 200) {
                return true;
            }
        }
        return false;
    }

    public int status(String url) {
        try (HttpClient client = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(2)).build()) {
            HttpResponse<String> r = client.send(HttpRequest.newBuilder(URI.create(url)).header("x-caller", name)
                    .timeout(Duration.ofSeconds(5)).build(), HttpResponse.BodyHandlers.ofString());
            return r.statusCode();
        } catch (Exception e) {
            return 0;
        }
    }
}
