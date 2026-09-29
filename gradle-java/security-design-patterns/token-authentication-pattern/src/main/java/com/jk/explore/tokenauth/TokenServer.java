package com.jk.explore.tokenauth;

/**
 * After: a server that keeps no sessions. It checks the token on each request with the shared key.
 */
public final class TokenServer {

    private final TokenService tokens;

    public TokenServer(TokenService tokens) {
        this.tokens = tokens;
    }

    public String cart(String token, long now) {
        Verdict v = tokens.verify(token, now);
        return v.valid() ? "200 " + v.customer() + "'s cart" : "401 " + v.reason();
    }
}
