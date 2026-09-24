package com.jk.explore.claimchecks3;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * The ticket: which bucket, which key, optionally which version, how big, and a checksum to
 * prove the luggage fetched is the luggage that was stored.
 *
 * <p>This small piece of text is the only thing that travels through the queue.
 */
public record Claim(String bucket, String key, String versionId, int size, String sha256) {

    /** The first 16 hex characters of the SHA-256 of the bytes: enough to notice any change. */
    public static String checksum(byte[] data) {
        try {
            return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(data)).substring(0, 16);
        } catch (NoSuchAlgorithmException e) {
            throw new IllegalStateException(e);
        }
    }

    /** The text that actually travels, as JSON. */
    public String toText() {
        return "{\"bucket\":\"" + bucket + "\",\"key\":\"" + key + "\""
                + (versionId == null ? "" : ",\"version\":\"" + versionId + "\"")
                + ",\"size\":" + size + ",\"sha256\":\"" + sha256 + "\"}";
    }

    /** How many bytes the ticket takes on the queue. */
    public int bytesOnTheQueue() {
        return toText().getBytes(StandardCharsets.UTF_8).length;
    }

    public static Claim read(String text) {
        String version = field(text, "version");
        return new Claim(field(text, "bucket"), field(text, "key"), version,
                Integer.parseInt(field(text, "size")), field(text, "sha256"));
    }

    private static String field(String text, String name) {
        Matcher m = Pattern.compile("\"" + name + "\":\"?([^\",}]+)").matcher(text);
        return m.find() ? m.group(1) : null;
    }
}
