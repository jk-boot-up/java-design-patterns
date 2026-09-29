package com.jk.explore.tokenauth;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: sessions stuck on one server, a signed token any server can check, tampering and
 * expiry, signing out early, and the bill.
 */
public final class TokenAuthDemo {

    static final long NOW = 1_000_000;
    static final String SECRET = "demo-only-secret-keep-real-keys-in-a-secrets-manager";

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. Sessions kept in one server's memory.");
        SessionServer a = new SessionServer("A");
        SessionServer b = new SessionServer("B");
        String session = a.signIn("ana");
        out.add("  ana signs in on server A, and gets session " + session);
        out.add("  next request, routed to A: " + a.cart(session));
        out.add("  next request, routed to B: " + b.cart(session));

        out.add("");
        out.add("TWO. A signed token: any server with the key can check it.");
        TokenService tokens = new TokenService(SECRET);
        TokenServer serverA = new TokenServer(tokens);
        TokenServer serverB = new TokenServer(new TokenService(SECRET));
        String token = tokens.issue("ana", NOW, 15 * 60);
        out.add("  token payload: " + TokenService.payloadOf(token));
        out.add("  server A: " + serverA.cart(token, NOW + 60));
        out.add("  server B: " + serverB.cart(token, NOW + 60) + "  (no shared session store)");

        out.add("");
        out.add("THREE. Forged and expired tokens are refused.");
        String forged = TokenService.withPayload(token, TokenService.payloadOf(token).replace("ana", "ben"));
        out.add("  payload changed to ben: " + serverA.cart(forged, NOW + 60));
        out.add("  used after 15 minutes:  " + serverA.cart(token, NOW + 15 * 60));

        out.add("");
        out.add("FOUR. Signing out early.");
        String laptop = tokens.issue("ana", NOW, 15 * 60);
        out.add("  ana signs out; the token alone still says: " + serverB.cart(laptop, NOW + 60));
        tokens.revoke(laptop);
        out.add("  with a revoked list, server A: " + serverA.cart(laptop, NOW + 60));
        out.add("  but server B has its own list: " + serverB.cart(laptop, NOW + 60));
        out.add("  so keep tokens short-lived, and share any revoked list");

        out.add("");
        out.add("FIVE. The bill: the key, and what the token shows.");
        out.add("  the payload is only encoded, not hidden: anyone can read " + TokenService.payloadOf(token));
        out.add("  and anyone who steals the key can sign a token for any customer");
        return out;
    }

    private TokenAuthDemo() {
    }
}
