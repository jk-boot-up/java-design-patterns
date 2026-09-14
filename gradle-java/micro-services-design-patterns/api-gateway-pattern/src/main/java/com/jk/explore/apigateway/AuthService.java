package com.jk.explore.apigateway;

/**
 * Checks an access token and says who is asking.
 *
 * Every service in the shop insists on this before it answers, which is
 * reasonable of them and is also the thing that makes calling four services
 * from a phone so tedious. Counting the checks is how the demo shows the
 * difference: the gateway checks once at the edge and is then trusted inside
 * the data centre, while a client calling four services checks four times.
 */
public final class AuthService {

    private static final String VALID_TOKEN = "tok-abc123";

    private int checks;

    public Customer check(String token) {
        checks++;
        if (!VALID_TOKEN.equals(token)) {
            throw new IllegalArgumentException("not signed in");
        }
        return new Customer("CUST-001");
    }

    /** How many tokens have been checked. */
    public int checks() {
        return checks;
    }

    /** The token the demo's signed-in shopper is carrying. */
    public static String validToken() {
        return VALID_TOKEN;
    }
}
