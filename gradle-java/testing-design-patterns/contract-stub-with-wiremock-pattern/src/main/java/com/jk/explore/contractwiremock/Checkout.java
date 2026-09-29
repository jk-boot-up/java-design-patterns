package com.jk.explore.contractwiremock;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

/**
 * The consumer: checkout posts a charge to whatever payment address it is given, and reads the reply.
 */
public final class Checkout {

    private static final HttpClient HTTP = HttpClient.newHttpClient();
    private final String paymentsUrl;

    public Checkout(String paymentsUrl) {
        this.paymentsUrl = paymentsUrl;
    }

    public String pay(String amount, String card, String currency) throws Exception {
        String body = "{\"amount\":\"" + amount + "\",\"card\":\"" + card + "\",\"currency\":\"" + currency + "\"}";
        HttpResponse<String> r = HTTP.send(HttpRequest.newBuilder(URI.create(paymentsUrl + "/charges"))
                .header("Content-Type", "application/json").POST(HttpRequest.BodyPublishers.ofString(body)).build(),
                HttpResponse.BodyHandlers.ofString());
        if (r.statusCode() == 404) {
            return "404 from the stub: " + (r.body().contains("Request was not matched") ? "Request was not matched" : r.body());
        }
        String result = PaymentService.value(r.body(), "result");
        if (result == null) {
            return "order stuck: no result in the reply";
        }
        return switch (result) {
            case "APPROVED" -> "order confirmed";
            case "DECLINED" -> "card declined: " + PaymentService.value(r.body(), "reason");
            default -> "payment rejected: " + PaymentService.value(r.body(), "reason");
        };
    }
}
