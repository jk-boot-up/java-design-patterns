package com.jk.explore.gatewayoffloading;

/**
 * Before: each service checks the sign-in token itself, and each team wrote its own copy of the check.
 */
public final class SelfCheckingService implements Service {

    private final String name;
    private final boolean checksExpiry;
    private final long now;

    public SelfCheckingService(String name, boolean checksExpiry, long now) {
        this.name = name;
        this.checksExpiry = checksExpiry;
        this.now = now;
    }

    @Override
    public Response handle(Request request) {
        String token = request.header("Authorization");
        String customer = Tokens.customer(token);
        if (customer == null) {
            return Response.of(401, "sign in");
        }
        if (checksExpiry && Tokens.expired(token, now)) {    // the orders team forgot this line
            return Response.of(401, "token expired");
        }
        return Response.of(200, name + " for " + customer);
    }
}
