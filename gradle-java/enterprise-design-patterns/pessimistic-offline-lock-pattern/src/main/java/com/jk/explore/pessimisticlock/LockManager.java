package com.jk.explore.pessimisticlock;

import java.time.Duration;
import java.util.HashMap;
import java.util.Map;

/**
 * Exclusive locks on named resources, held by an owner until released or until they expire. Whoever
 * holds the lock may edit; everyone else is told who does.
 */
public class LockManager {

    private record Held(String owner, long expiresAt) {
    }

    private final Map<String, Held> held = new HashMap<>();
    private final Clock clock;

    public LockManager(Clock clock) {
        this.clock = clock;
    }

    public synchronized void acquire(String resource, String owner, Duration timeToLive) {
        Held current = held.get(resource);
        if (current != null && current.expiresAt() > clock.now() && !current.owner().equals(owner)) {
            throw new LockedBy(resource, current.owner());
        }
        held.put(resource, new Held(owner, clock.now() + timeToLive.toMinutes()));
    }

    public synchronized boolean holds(String resource, String owner) {
        Held current = held.get(resource);
        return current != null && current.owner().equals(owner) && current.expiresAt() > clock.now();
    }

    public synchronized void release(String resource, String owner) {
        if (holds(resource, owner)) {
            held.remove(resource);
        }
    }
}
