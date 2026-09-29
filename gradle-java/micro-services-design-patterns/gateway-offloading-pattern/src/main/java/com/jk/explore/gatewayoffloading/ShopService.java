package com.jk.explore.gatewayoffloading;

/**
 * After: the service only does its own job. It trusts the customer the gateway has already checked.
 */
public final class ShopService implements Service {

    private final String name;
    private final String body;
    private int calls;

    public ShopService(String name, String body) {
        this.name = name;
        this.body = body;
    }

    @Override
    public Response handle(Request request) {
        calls++;
        return Response.of(200, body.isEmpty() ? name + " for " + request.header("X-Customer") : body);
    }

    public int calls() {
        return calls;
    }
}
