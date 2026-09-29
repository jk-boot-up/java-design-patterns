package com.jk.explore.securenginx;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: a real order service, and a real NGINX gatekeeper in front of it.
 */
public final class NginxSecureGatewayDemo {

    static final HttpClient HTTP = HttpClient.newHttpClient();

    public static void main(String[] args) throws Exception {
        if (!Gatekeeper.containerRuntimeAvailable()) {
            System.out.println(Gatekeeper.NO_RUNTIME_ADVICE);
            return;
        }
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        try (OrderService orders = new OrderService()) {

            out.add("ONE. The order service faces the internet directly.");
            out.add("  GET /orders/7:                     " + call("GET", orders.url() + "/orders/7", null, 0));
            out.add("  with header X-Internal-Admin=true: " + call("GET", orders.url() + "/orders/7", "true", 0));
            out.add("  GET /orders/../admin/export:       " + call("GET", orders.url() + "/orders/../admin/export", null, 0));
            out.add("  and this machine holds the database password");

            try (Gatekeeper gate = new Gatekeeper(orders.port())) {
                try {
                    gate.start();
                } catch (RuntimeException e) {
                    out.add(Gatekeeper.WOULD_NOT_START_ADVICE);
                    return out;
                }
                String g = gate.url();

                out.add("");
                out.add("TWO. An NGINX gatekeeper in front; only it faces the internet.");
                out.add("  GET /orders/7:                     " + call("GET", g + "/orders/7", null, 0));
                out.add("  with header X-Internal-Admin=true: " + call("GET", g + "/orders/7", "true", 0));
                out.add("  proxy_set_header X-Internal-Admin \"\" removed the header on the way through");

                out.add("");
                out.add("THREE. Only allowed shapes of request pass.");
                out.add("  GET /orders/../admin/export: " + call("GET", g + "/orders/../admin/export", null, 0)
                        + "  (NGINX tidies the path first, then no location matches)");
                out.add("  DELETE /orders/7:            " + call("DELETE", g + "/orders/7", null, 0)
                        + "  (limit_except GET)");
                out.add("  POST /orders:                " + call("POST", g + "/orders", null, 800));

                out.add("");
                out.add("FOUR. Size and shape limits.");
                out.add("  POST /orders, 5 MB body: " + call("POST", g + "/orders", null, 5_000_000) + "  (client_max_body_size 1m)");
                out.add("  GET /orders/7 OR 1=1:    " + call("GET", g + "/orders/7%20OR%201=1", null, 0) + "  (the number must be digits)");

                out.add("");
                out.add("FIVE. The bill.");
                out.add("  the NGINX container's environment holds credentials: " + gate.holdsCredentials());
                out.add("  every request pays an extra hop, and a new endpoint is blocked until the configuration allows it");
                out.add("  and the order service must still check its own inputs: the gate is one layer, not the only one");
            }
        }
        return out;
    }

    static String call(String method, String url, String adminHeader, int bodyBytes) throws Exception {
        HttpRequest.Builder r = HttpRequest.newBuilder(URI.create(url))
                .method(method, bodyBytes > 0 ? HttpRequest.BodyPublishers.ofByteArray(new byte[bodyBytes])
                        : HttpRequest.BodyPublishers.noBody());
        if (adminHeader != null) {
            r.header("X-Internal-Admin", adminHeader);
        }
        HttpResponse<String> response = HTTP.send(r.build(), HttpResponse.BodyHandlers.ofString());
        String body = response.body().contains("<html>") ? reason(response.statusCode()) : response.body();
        return response.statusCode() + " " + body;
    }

    private static String reason(int status) {
        return switch (status) {
            case 403 -> "forbidden";
            case 404 -> "not found";
            case 413 -> "too large";
            default -> "";
        };
    }

    private NginxSecureGatewayDemo() {
    }
}
