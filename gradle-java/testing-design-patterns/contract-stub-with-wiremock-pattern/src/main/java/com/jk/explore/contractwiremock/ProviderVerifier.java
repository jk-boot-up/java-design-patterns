package com.jk.explore.contractwiremock;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.List;

/**
 * The other half, run in the payment team's build: replays every interaction in the contract against
 * the real service over HTTP, and reports each reply that differs.
 */
public final class ProviderVerifier {

    private static final HttpClient HTTP = HttpClient.newHttpClient();

    public static List<String> mismatches(Contract contract, String serviceUrl) throws Exception {
        List<String> problems = new ArrayList<>();
        for (Contract.Interaction i : contract.interactions()) {
            HttpResponse<String> r = HTTP.send(HttpRequest.newBuilder(URI.create(serviceUrl + i.url()))
                    .header("Content-Type", "application/json")
                    .method(i.method(), HttpRequest.BodyPublishers.ofString(i.requestBody())).build(),
                    HttpResponse.BodyHandlers.ofString());
            if (r.statusCode() != i.status() || !r.body().equals(i.responseBody())) {
                problems.add(i.description());
            }
        }
        return problems;
    }

    private ProviderVerifier() {
    }
}
