package com.jk.explore.offloadgateway;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

/**
 * The five acts: three real back-end services and a real Spring Cloud Gateway in front of them.
 */
public final class GatewayOffloadingSpringDemo {

    static final HttpClient HTTP = HttpClient.newHttpClient();

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        long now = Instant.now().getEpochSecond();
        String expired = Tokens.issue("ana", now - 60);
        String valid = Tokens.issue("ana", now + 3600);

        out.add("ONE. Every service checks the sign-in token itself.");
        try (ShopService catalog = new ShopService("catalog", ShopService.Mode.CHECKS_TOKEN, "");
             ShopService cart = new ShopService("cart", ShopService.Mode.CHECKS_TOKEN, "");
             ShopService orders = new ShopService("orders", ShopService.Mode.FORGETS_EXPIRY, "")) {
            out.add("  expired token -> catalog: " + show(get(catalog.url() + "/catalog", expired, null)));
            out.add("  expired token -> cart:    " + show(get(cart.url() + "/cart", expired, null)));
            out.add("  expired token -> orders:  " + show(get(orders.url() + "/orders", expired, null)));
            out.add("  three copies of the same check, and the orders team forgot expiry");
        }

        StringBuilder json = new StringBuilder("[");
        for (int i = 1; i <= 200; i++) {
            json.append("{\"sku\":\"SKU-").append(i).append("\",\"name\":\"Coffee mug\",\"price\":9.99},");
        }
        json.setCharAt(json.length() - 1, ']');

        try (ShopService catalog = new ShopService("catalog", ShopService.Mode.TRUSTS_GATEWAY, json.toString());
             ShopService cart = new ShopService("cart", ShopService.Mode.TRUSTS_GATEWAY, "");
             ShopService orders = new ShopService("orders", ShopService.Mode.TRUSTS_GATEWAY, "");
             ConfigurableApplicationContext gateway = new SpringApplicationBuilder(GatewayApp.class)
                     .properties("server.port=0", "spring.main.banner-mode=off", "logging.level.root=OFF",
                             "server.compression.enabled=true", "server.compression.mime-types=application/json",
                             "server.compression.min-response-size=1KB",
                             "shop.catalog=" + catalog.url(), "shop.cart=" + cart.url(), "shop.orders=" + orders.url())
                     .run()) {
            String gw = "http://127.0.0.1:" + gateway.getEnvironment().getProperty("local.server.port");
            SignInFilter limiter = gateway.getBean(SignInFilter.class);

            out.add("");
            out.add("TWO. Spring Cloud Gateway checks the token once, for every service.");
            out.add("  expired token -> catalog: " + show(get(gw + "/catalog", expired, null)));
            out.add("  expired token -> cart:    " + show(get(gw + "/cart", expired, null)));
            out.add("  expired token -> orders:  " + show(get(gw + "/orders", expired, null)));
            out.add("  valid token -> orders:    " + show(get(gw + "/orders", valid, null)));
            out.add("  the services behind hold no sign-in code at all");

            out.add("");
            out.add("THREE. The gateway limits each customer to " + SignInFilter.PER_MINUTE + " requests a minute.");
            limiter.reset();
            int passed = 0;
            int refused = 0;
            for (int i = 0; i < 8; i++) {
                if (get(gw + "/orders", valid, null).statusCode() == 429) {
                    refused++;
                } else {
                    passed++;
                }
            }
            out.add("  8 requests in a row: " + passed + " passed, " + refused + " refused with 429");

            out.add("");
            out.add("FOUR. Reactor Netty compresses responses at the gateway.");
            limiter.reset();
            HttpResponse<byte[]> plain = getBytes(gw + "/catalog", valid, false);
            HttpResponse<byte[]> zipped = getBytes(gw + "/catalog", valid, true);
            out.add("  catalog page: " + plain.body().length + " bytes plain, "
                    + (zipped.body().length < plain.body().length / 5 ? "under a fifth of that" : "barely smaller")
                    + " with Content-Encoding " + zipped.headers().firstValue("Content-Encoding").orElse("none"));
            out.add("  the catalog service knows nothing about compression");

            out.add("");
            out.add("FIVE. The bill: what the services now trust.");
            limiter.reset();
            out.add("  through the gateway, ana's token plus a spoofed X-Customer: ben -> "
                    + show(get(gw + "/orders", valid, "ben")));
            out.add("  straight to the orders service, X-Customer: ben -> " + show(get(orders.url() + "/orders", null, "ben")));
            out.add("  the services must be reachable only through the gateway; and every request now passes one more hop");
        }
        return out;
    }

    static HttpResponse<String> get(String url, String token, String customerHeader) throws Exception {
        HttpRequest.Builder r = HttpRequest.newBuilder(URI.create(url)).GET();
        if (token != null) {
            r.header("Authorization", token);
        }
        if (customerHeader != null) {
            r.header("X-Customer", customerHeader);
        }
        return HTTP.send(r.build(), HttpResponse.BodyHandlers.ofString());
    }

    static HttpResponse<byte[]> getBytes(String url, String token, boolean gzip) throws Exception {
        HttpRequest.Builder r = HttpRequest.newBuilder(URI.create(url)).GET().header("Authorization", token);
        if (gzip) {
            r.header("Accept-Encoding", "gzip");
        }
        return HTTP.send(r.build(), HttpResponse.BodyHandlers.ofByteArray());
    }

    static String show(HttpResponse<String> r) {
        return r.statusCode() + " " + r.body();
    }

    private GatewayOffloadingSpringDemo() {
    }
}
