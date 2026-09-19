package com.jk.explore.pactcdc;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** The checkout's own code for reading a price. It reads sku and priceCents, and nothing else. */
public class CheckoutClient {

    private static final Pattern PRICE = Pattern.compile("\"priceCents\"\\s*:\\s*(\\d+)");

    private final String baseUrl;

    public CheckoutClient(String baseUrl) {
        this.baseUrl = baseUrl;
    }

    /** The total in cents, or -1 if the answer was not what checkout needs. */
    public long total(String sku, int quantity) {
        try (HttpClient client = HttpClient.newHttpClient()) {
            HttpResponse<String> r = client.send(HttpRequest.newBuilder(URI.create(baseUrl + "/prices/" + sku)).build(), HttpResponse.BodyHandlers.ofString());
            Matcher m = PRICE.matcher(r.body());
            return m.find() ? Long.parseLong(m.group(1)) * quantity : -1;
        } catch (Exception e) {
            return -1;
        }
    }
}
