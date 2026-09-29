package com.jk.explore.gatewayoffloading;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: every service checks for itself, one check at the gateway, rate limiting,
 * compression, and the bill.
 */
public final class GatewayOffloadingDemo {

    static final long NOW = 1_000;

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();
        String expired = Tokens.issue("ana", NOW - 60);
        String valid = Tokens.issue("ana", NOW + 3600);

        out.add("ONE. Every service checks the sign-in token itself.");
        List<SelfCheckingService> before = List.of(
                new SelfCheckingService("catalog", true, NOW),
                new SelfCheckingService("cart", true, NOW),
                new SelfCheckingService("orders", false, NOW));
        String[] names = {"catalog", "cart", "orders"};
        for (int i = 0; i < 3; i++) {
            Response r = before.get(i).handle(Request.of("/" + names[i], "Authorization", expired));
            out.add("  expired token -> " + names[i] + ": " + r.status() + " " + r.text());
        }
        out.add("  three copies of the same check, and the orders team forgot expiry");

        out.add("");
        out.add("TWO. The gateway checks the token once, for every service.");
        ShopService catalog = new ShopService("catalog", "");
        ShopService cart = new ShopService("cart", "");
        ShopService orders = new ShopService("orders", "");
        Gateway gateway = new Gateway(NOW, 5)
                .route("/catalog", catalog).route("/cart", cart).route("/orders", orders);
        for (String name : names) {
            Response r = gateway.handle(Request.of("/" + name, "Authorization", expired));
            out.add("  expired token -> " + name + ": " + r.status() + " " + r.text());
        }
        Response ok = gateway.handle(Request.of("/orders", "Authorization", valid));
        out.add("  valid token -> orders: " + ok.status() + " " + ok.text());
        out.add("  the services hold no sign-in code at all");

        out.add("");
        out.add("THREE. The gateway limits each customer to 5 requests a second.");
        gateway.tick(NOW + 1);
        int before429 = orders.calls();
        int allowed = 0;
        int refused = 0;
        for (int i = 0; i < 8; i++) {
            if (gateway.handle(Request.of("/orders", "Authorization", valid)).status() == 429) {
                refused++;
            } else {
                allowed++;
            }
        }
        out.add("  8 requests in one second: " + allowed + " passed, " + refused + " refused with 429");
        out.add("  the orders service saw " + (orders.calls() - before429));

        out.add("");
        out.add("FOUR. The gateway compresses responses.");
        StringBuilder json = new StringBuilder("[");
        for (int i = 1; i <= 200; i++) {
            json.append("{\"sku\":\"SKU-").append(i).append("\",\"name\":\"Coffee mug\",\"price\":9.99},");
        }
        json.append("]");
        Gateway shop = new Gateway(NOW, 5).route("/catalog", new ShopService("catalog", json.toString()));
        Response plain = shop.handle(Request.of("/catalog", "Authorization", valid));
        Response zipped = shop.handle(Request.of("/catalog", "Authorization", valid, "Accept-Encoding", "gzip"));
        out.add("  catalog page: " + plain.body().length + " bytes plain, "
                + (zipped.body().length < plain.body().length / 5 ? "under a fifth of that" : "barely smaller")
                + " gzipped");
        out.add("  one gzip at the gateway, not one in every service");

        out.add("");
        out.add("FIVE. The bill: everything goes through one place.");
        Response bypass = orders.handle(Request.of("/orders", "X-Customer", "ben"));
        out.add("  a call straight to the orders service, claiming to be ben: " + bypass.status() + " " + bypass.text());
        out.add("  services must only be reachable through the gateway");
        out.add("  and a gateway fault, or a slow gateway, hits every page at once");
        return out;
    }

    private GatewayOffloadingDemo() {
    }
}
