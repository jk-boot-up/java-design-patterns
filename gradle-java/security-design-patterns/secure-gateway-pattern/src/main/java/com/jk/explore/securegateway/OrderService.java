package com.jk.explore.securegateway;

import java.net.URI;

/**
 * The trusted back-end service. It holds the database password and has internal features
 * (an admin export, an internal-tools header) that were never meant for the public.
 */
public final class OrderService {

    private final String databasePassword;

    public OrderService(String databasePassword) {
        this.databasePassword = databasePassword;
    }

    public String handle(HttpRequest request) {
        String path = URI.create(request.path()).normalize().getPath();   // "/orders/../admin" becomes "/admin"
        if ("true".equals(request.headers().get("X-Internal-Admin")) || path.equals("/admin/export")) {
            return "200 export of all 12000 orders";
        }
        if (request.method().equals("GET") && path.startsWith("/orders/")) {
            return "200 order " + path.substring("/orders/".length());
        }
        if (request.method().equals("POST") && path.equals("/orders")) {
            return "201 order created";
        }
        return "404 not found";
    }

    boolean hasCredentials() {
        return databasePassword != null;
    }
}
