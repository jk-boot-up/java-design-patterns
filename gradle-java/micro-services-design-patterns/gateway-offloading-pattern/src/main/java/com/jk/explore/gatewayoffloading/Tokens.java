package com.jk.explore.gatewayoffloading;

/**
 * Sign-in tokens of the form {@code tok:<customer>:<expires-at-second>}. A real system would use signed JWTs.
 */
public final class Tokens {

    public static String issue(String customer, long expiresAt) {
        return "tok:" + customer + ":" + expiresAt;
    }

    /** The customer, or null if the token is malformed. Does not look at expiry. */
    public static String customer(String token) {
        if (token == null || !token.startsWith("tok:")) {
            return null;
        }
        return token.split(":")[1];
    }

    public static boolean expired(String token, long now) {
        return Long.parseLong(token.split(":")[2]) <= now;
    }

    private Tokens() {
    }
}
