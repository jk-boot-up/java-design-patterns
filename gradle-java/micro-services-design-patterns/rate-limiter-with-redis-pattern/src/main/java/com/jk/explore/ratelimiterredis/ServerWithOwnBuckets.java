package com.jk.explore.ratelimiterredis;

import io.github.bucket4j.Bucket;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * One copy of the shop's search service, keeping its buckets in its own memory.
 *
 * <p>This is the plain-Java twin's rate limiter, written with Bucket4j's in-memory bucket.
 * On one server it is exactly right. On three it is three separate limits that know nothing
 * about each other.
 */
public class ServerWithOwnBuckets {

    private final Map<String, Bucket> buckets = new ConcurrentHashMap<>();

    public boolean search(String clientId) {
        return buckets.computeIfAbsent(clientId, id -> SearchLimit.inMemoryBucket()).tryConsume(1);
    }

    public int bucketsHeld() {
        return buckets.size();
    }
}
