package com.jk.explore.tokenauth;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class TokenServiceTest {

    private final TokenService tokens = new TokenService("k1");

    @Test
    void roundTrip() {
        Verdict v = tokens.verify(tokens.issue("zoe", 0, 10), 5);
        assertTrue(v.valid());
        assertEquals("zoe", v.customer());
    }

    @Test
    void otherKeyCannotVerify() {
        String t = new TokenService("k2").issue("zoe", 0, 10);
        assertEquals("bad signature", tokens.verify(t, 5).reason());
    }

    @Test
    void malformedIsRefused() {
        assertEquals("malformed", tokens.verify("abc", 5).reason());
    }

    @Test
    void expiryIsExclusive() {
        assertEquals("expired", tokens.verify(tokens.issue("zoe", 0, 10), 10).reason());
    }
}
