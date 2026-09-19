package com.jk.explore.leaderelection;

import java.util.Optional;

/**
 * One shared record saying who leads. A node may take the lease if nobody holds it or the holder's has expired,
 * and the current holder may renew it. Each change of holder raises the token by one.
 */
public class LeaseStore {

    private final Clock clock;
    private Lease current;
    private long lastToken;

    public LeaseStore(Clock clock) {
        this.clock = clock;
    }

    public synchronized Optional<Lease> acquireOrRenew(String node, long ttlSeconds) {
        boolean free = current == null || current.expiresAt() <= clock.now();
        if (free) {
            current = new Lease(node, ++lastToken, clock.now() + ttlSeconds);
            return Optional.of(current);
        }
        if (current.holder().equals(node)) {
            current = new Lease(node, current.token(), clock.now() + ttlSeconds);
            return Optional.of(current);
        }
        return Optional.empty();
    }

    public synchronized Optional<String> leader() {
        return current != null && current.expiresAt() > clock.now() ? Optional.of(current.holder()) : Optional.empty();
    }
}
