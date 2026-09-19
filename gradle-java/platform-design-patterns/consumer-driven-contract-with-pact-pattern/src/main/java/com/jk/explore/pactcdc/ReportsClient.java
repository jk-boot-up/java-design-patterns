package com.jk.explore.pactcdc;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** Another consumer. It reads only the sku. */
public class ReportsClient {

    private static final Pattern SKU = Pattern.compile("\"sku\"\\s*:\\s*\"([^\"]+)\"");

    private final String baseUrl;

    public ReportsClient(String baseUrl) {
        this.baseUrl = baseUrl;
    }

    public String skuOf(String sku) {
        try (HttpClient client = HttpClient.newHttpClient()) {
            HttpResponse<String> r = client.send(HttpRequest.newBuilder(URI.create(baseUrl + "/prices/" + sku)).build(), HttpResponse.BodyHandlers.ofString());
            Matcher m = SKU.matcher(r.body());
            return m.find() ? m.group(1) : null;
        } catch (Exception e) {
            return null;
        }
    }
}
