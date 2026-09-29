package com.jk.explore.tokenauth;

import java.nio.charset.StandardCharsets;
import java.security.GeneralSecurityException;
import java.security.MessageDigest;
import java.util.Base64;
import java.util.HashSet;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

/**
 * The pattern: a signed token in the same shape as a JWT, header.payload.signature.
 * The payload says who the customer is and when the token expires; the HMAC-SHA256 signature
 * proves the shop issued it. Any server holding the key can check it without asking anyone.
 */
public final class TokenService {

    private static final String HEADER = encode("{\"alg\":\"HS256\",\"typ\":\"JWT\"}");
    private static final Pattern FIELD = Pattern.compile("\"(\\w+)\":\"?([^\",}]*)");

    private final byte[] key;
    private final Set<String> revoked = new HashSet<>();
    private int next = 1;

    public TokenService(String secret) {
        this.key = secret.getBytes(StandardCharsets.UTF_8);
    }

    public String issue(String customer, long now, long lifetimeSeconds) {
        String payload = encode("{\"sub\":\"" + customer + "\",\"exp\":" + (now + lifetimeSeconds)
                + ",\"jti\":\"t" + next++ + "\"}");
        return HEADER + "." + payload + "." + sign(HEADER + "." + payload);
    }

    public Verdict verify(String token, long now) {
        String[] parts = token.split("\\.");
        if (parts.length != 3) {
            return Verdict.refused("malformed");
        }
        byte[] expected = sign(parts[0] + "." + parts[1]).getBytes(StandardCharsets.UTF_8);
        if (!MessageDigest.isEqual(expected, parts[2].getBytes(StandardCharsets.UTF_8))) {
            return Verdict.refused("bad signature");
        }
        String payload = decode(parts[1]);
        if (Long.parseLong(field(payload, "exp")) <= now) {
            return Verdict.refused("expired");
        }
        if (revoked.contains(field(payload, "jti"))) {
            return Verdict.refused("revoked");
        }
        return Verdict.ok(field(payload, "sub"));
    }

    /** Signing out early: remember the token's identifier until it would have expired anyway. */
    public void revoke(String token) {
        revoked.add(field(decode(token.split("\\.")[1]), "jti"));
    }

    public static String payloadOf(String token) {
        return decode(token.split("\\.")[1]);
    }

    public static String withPayload(String token, String payload) {
        String[] parts = token.split("\\.");
        return parts[0] + "." + encode(payload) + "." + parts[2];
    }

    private String sign(String data) {
        try {
            Mac mac = Mac.getInstance("HmacSHA256");
            mac.init(new SecretKeySpec(key, "HmacSHA256"));
            return Base64.getUrlEncoder().withoutPadding().encodeToString(mac.doFinal(data.getBytes(StandardCharsets.UTF_8)));
        } catch (GeneralSecurityException e) {
            throw new IllegalStateException(e);
        }
    }

    private static String field(String json, String name) {
        Matcher m = FIELD.matcher(json);
        while (m.find()) {
            if (m.group(1).equals(name)) {
                return m.group(2);
            }
        }
        throw new IllegalArgumentException("no " + name);
    }

    private static String encode(String text) {
        return Base64.getUrlEncoder().withoutPadding().encodeToString(text.getBytes(StandardCharsets.UTF_8));
    }

    private static String decode(String text) {
        return new String(Base64.getUrlDecoder().decode(text), StandardCharsets.UTF_8);
    }
}
