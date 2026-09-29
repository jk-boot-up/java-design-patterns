package com.jk.explore.offloadgateway;

/**
 * Sign-in tokens of the form {@code tok:<customer>:<expires-at-epoch-second>}. A real shop would use signed JWTs.
 */
public final class Tokens {

    public static String issue(String customer, long expiresAt) {
        return "tok:" + customer + ":" + expiresAt;
    }

    /** The customer, or null if the token is missing or malformed. Does not look at expiry. */
    public static String customer(String token) {
        if (token == null || !token.startsWith("tok:") || token.split(":").length != 3) {
            return null;
        }
        return token.split(":")[1];
    }

    public static boolean expired(String token, long nowSecond) {
        return Long.parseLong(token.split(":")[2]) <= nowSecond;
    }

    private Tokens() {
    }
}
