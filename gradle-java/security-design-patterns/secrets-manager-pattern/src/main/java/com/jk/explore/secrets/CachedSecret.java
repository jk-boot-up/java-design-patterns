package com.jk.explore.secrets;

/**
 * How a service holds a secret: fetched from the manager, kept for a few minutes, then fetched again,
 * so a rotation reaches every service without a restart.
 */
public final class CachedSecret {

    private final SecretsManager manager;
    private final String service;
    private final String name;
    private final long ttlSeconds;
    private String value;
    private long fetchedAt = Long.MIN_VALUE;

    public CachedSecret(SecretsManager manager, String service, String name, long ttlSeconds) {
        this.manager = manager;
        this.service = service;
        this.name = name;
        this.ttlSeconds = ttlSeconds;
    }

    public String get(long now) {
        if (value == null || now - fetchedAt >= ttlSeconds) {
            value = manager.read(service, name);
            fetchedAt = now;
        }
        return value;
    }

    /** Throws the cached copy away, for when the key has just been refused. */
    public String refresh(long now) {
        value = null;
        return get(now);
    }
}
