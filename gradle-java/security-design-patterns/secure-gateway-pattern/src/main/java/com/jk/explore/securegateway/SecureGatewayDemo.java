package com.jk.explore.securegateway;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * The five acts: the trusted service on the internet, a gatekeeper in front, an allow-list,
 * size and shape limits, and the bill.
 */
public final class SecureGatewayDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();
        OrderService orders = new OrderService("s3cret-db-password");
        HttpRequest spoof = new HttpRequest("GET", "/orders/7", Map.of("X-Internal-Admin", "true"), 0);
        HttpRequest traversal = HttpRequest.get("/orders/../admin/export");

        out.add("ONE. The order service faces the internet directly.");
        out.add("  GET /orders/7:                     " + orders.handle(HttpRequest.get("/orders/7")));
        out.add("  with header X-Internal-Admin=true: " + orders.handle(spoof));
        out.add("  GET /orders/../admin/export:       " + orders.handle(traversal));
        out.add("  and this internet-facing machine holds the database password: " + orders.hasCredentials());

        out.add("");
        out.add("TWO. A gatekeeper in front; only it faces the internet.");
        Gatekeeper gate = new Gatekeeper(orders);
        out.add("  GET /orders/7:                     " + gate.handle(HttpRequest.get("/orders/7")));
        out.add("  with header X-Internal-Admin=true: " + gate.handle(spoof));
        out.add("  internal headers are stripped at the gate");

        out.add("");
        out.add("THREE. Only allowed shapes of request pass.");
        out.add("  GET /orders/../admin/export: " + gate.handle(traversal));
        out.add("  DELETE /orders/7:            " + gate.handle(new HttpRequest("DELETE", "/orders/7", Map.of(), 0)));
        out.add("  POST /orders:                " + gate.handle(new HttpRequest("POST", "/orders", Map.of(), 800)));

        out.add("");
        out.add("FOUR. Size and shape limits.");
        out.add("  POST /orders, 5 MB body: " + gate.handle(new HttpRequest("POST", "/orders", Map.of(), 5_000_000)));
        out.add("  GET /orders/7 OR 1=1:    " + gate.handle(HttpRequest.get("/orders/7 OR 1=1")));
        out.add("  passed " + gate.passed() + ", refused " + gate.refused());

        out.add("");
        out.add("FIVE. The bill: one more hop, and one more list to keep.");
        out.add("  if the gatekeeper is broken into, it holds credentials: " + gate.hasCredentials());
        out.add("  every request pays an extra hop");
        out.add("  and a new endpoint is blocked until someone adds it to the gate's list");
        return out;
    }

    private SecureGatewayDemo() {
    }
}
