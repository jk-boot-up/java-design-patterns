package com.jk.explore.claimcheck;

import java.util.HashMap;
import java.util.Map;
import java.security.SecureRandom;
import java.util.HexFormat;
import java.util.function.Supplier;

/** Cheap storage for big things. Every operation is counted, and a blob is kept for a limited time. */
public class BlobStore {

    private record Blob(byte[] data, long expiresAt) {
    }

    private final Map<String, Blob> blobs = new HashMap<>();
    private final Clock clock;
    private final long timeToLiveMinutes;
    private int operations;
    private final Supplier<String> ids;

    /** Claims that cannot be guessed: 128 random bits. */
    public static Supplier<String> unguessable() {
        SecureRandom random = new SecureRandom();
        return () -> {
            byte[] b = new byte[16];
            random.nextBytes(b);
            return "blob-" + HexFormat.of().formatHex(b);
        };
    }

    /** Claims that count up: blob-1, blob-2. Easy to write, and easy for anyone to guess. */
    public static Supplier<String> sequential() {
        int[] n = {0};
        return () -> "blob-" + (++n[0]);
    }

    public BlobStore(Clock clock, long timeToLiveMinutes) {
        this(clock, timeToLiveMinutes, unguessable());
    }

    public BlobStore(Clock clock, long timeToLiveMinutes, Supplier<String> ids) {
        this.clock = clock;
        this.timeToLiveMinutes = timeToLiveMinutes;
        this.ids = ids;
    }

    public String put(byte[] data) {
        operations++;
        String id = ids.get();
        blobs.put(id, new Blob(data.clone(), clock.now() + timeToLiveMinutes));
        return id;
    }

    public byte[] get(String id) {
        operations++;
        Blob b = blobs.get(id);
        if (b == null || b.expiresAt() <= clock.now()) {
            throw new ClaimExpired(id);
        }
        return b.data().clone();
    }

    public void delete(String id) {
        operations++;
        blobs.remove(id);
    }

    /** Test hook: change what is stored, as a fault or an attacker might. */
    public void tamper(String id) {
        blobs.get(id).data()[0] ^= 1;
    }

    public int stored() {
        return blobs.size();
    }

    public int operations() {
        return operations;
    }

    public int deleteExpired() {
        int before = blobs.size();
        blobs.values().removeIf(b -> b.expiresAt() <= clock.now());
        return before - blobs.size();
    }

    public static class ClaimExpired extends RuntimeException {
        public ClaimExpired(String id) {
            super("the blob for this claim expired or was never stored");
        }
    }
}
