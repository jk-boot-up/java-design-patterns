package com.jk.explore.ratelimiterredis;

import io.github.bucket4j.ConsumptionProbe;
import io.github.bucket4j.TimeMeter;
import io.github.bucket4j.distributed.ExpirationAfterWriteStrategy;
import io.github.bucket4j.distributed.proxy.ProxyManager;
import io.github.bucket4j.redis.lettuce.Bucket4jLettuce;
import io.lettuce.core.ClientOptions;
import io.lettuce.core.RedisClient;
import io.lettuce.core.api.StatefulRedisConnection;
import io.lettuce.core.codec.ByteArrayCodec;
import io.lettuce.core.codec.RedisCodec;
import io.lettuce.core.codec.StringCodec;
import java.time.Duration;

/**
 * One copy of the shop's search service, keeping its buckets in Redis.
 *
 * <p>Each server has its own connection to Redis, exactly as separate machines would. None
 * of them holds a bucket itself. On every search, Bucket4j reads the client's bucket from
 * Redis, works out on this server whether a token is there, and writes the new state back
 * only if nobody else changed it in between. If somebody did, it reads again and tries again.
 */
public class ServerSharingRedis implements AutoCloseable {

    private final String name;
    private final RedisClient client;
    private final StatefulRedisConnection<String, byte[]> connection;
    private final ProxyManager<String> buckets;

    /** A server whose clock is right. */
    public ServerSharingRedis(Redis redis, String name) {
        this(redis, name, Duration.ZERO);
    }

    /**
     * A server whose clock is wrong by the given amount. Bucket4j does its refill sums with
     * the clock of the server it runs on, not with Redis's clock, so this changes the answer.
     */
    public ServerSharingRedis(Redis redis, String name, Duration clockAhead) {
        this.name = name;
        this.client = RedisClient.create(redis.uri());
        // When Redis is gone, fail at once rather than queue the search and wait.
        this.client.setOptions(ClientOptions.builder()
                .disconnectedBehavior(ClientOptions.DisconnectedBehavior.REJECT_COMMANDS)
                .build());
        this.connection = client.connect(RedisCodec.of(StringCodec.UTF8, ByteArrayCodec.INSTANCE));
        this.buckets = Bucket4jLettuce.casBasedBuilder(connection)
                .clientClock(clockThatIsAheadBy(clockAhead))
                // Redis deletes a client's key by itself once the bucket would be full again,
                // because a full bucket and no bucket at all mean the same thing.
                .expirationAfterWrite(ExpirationAfterWriteStrategy.basedOnTimeForRefillingBucketUpToMax(Duration.ZERO))
                .requestTimeout(Duration.ofSeconds(5))
                .build();
    }

    public String name() {
        return name;
    }

    /** True if the search may go ahead, false if the client has no tokens left. */
    public boolean search(String clientId) {
        return buckets.getProxy(SearchLimit.keyFor(clientId), SearchLimit::configuration).tryConsume(1);
    }

    /** The same, and when refused, how long until a token comes back. */
    public ConsumptionProbe searchAndHearWhen(String clientId) {
        return buckets.getProxy(SearchLimit.keyFor(clientId), SearchLimit::configuration).tryConsumeAndReturnRemaining(1);
    }

    /** True while this server still has a live connection to Redis. */
    public boolean connected() {
        return connection.isOpen();
    }

    @Override
    public void close() {
        connection.close();
        client.shutdown(Duration.ZERO, Duration.ofSeconds(2));
    }

    private static TimeMeter clockThatIsAheadBy(Duration ahead) {
        long aheadNanos = ahead.toNanos();
        return new TimeMeter() {
            @Override
            public long currentTimeNanos() {
                return System.currentTimeMillis() * 1_000_000L + aheadNanos;
            }

            @Override
            public boolean isWallClockBased() {
                return true;
            }
        };
    }
}
