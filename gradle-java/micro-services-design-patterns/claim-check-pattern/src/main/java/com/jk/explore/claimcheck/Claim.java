package com.jk.explore.claimcheck;

import java.security.MessageDigest;
import java.util.HexFormat;

/** The ticket: where the luggage is, how big it is, and how to check it is the same luggage. */
public record Claim(String blobId, int size, String sha256) {

    public static String checksum(byte[] data) {
        try {
            return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(data)).substring(0, 16);
        } catch (java.security.NoSuchAlgorithmException e) {
            throw new IllegalStateException(e);
        }
    }

    /** A short text form, which is what actually travels through the broker. */
    public byte[] toBytes() {
        return (blobId + "|" + size + "|" + sha256).getBytes(java.nio.charset.StandardCharsets.UTF_8);
    }

    public static Claim fromBytes(byte[] bytes) {
        String[] p = new String(bytes, java.nio.charset.StandardCharsets.UTF_8).split("\\|");
        return new Claim(p[0], Integer.parseInt(p[1]), p[2]);
    }
}
