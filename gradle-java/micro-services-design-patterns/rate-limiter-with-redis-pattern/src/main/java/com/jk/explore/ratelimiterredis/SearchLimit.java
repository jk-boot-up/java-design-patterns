package com.jk.explore.ratelimiterredis;

import io.github.bucket4j.Bandwidth;
import io.github.bucket4j.Bucket;
import io.github.bucket4j.BucketConfiguration;
import java.time.Duration;

/**
 * The rule every shop server applies to product search: 10 searches per client, and the
 * bucket is filled back up to 10 once an hour.
 *
 * <p>The refill is once an hour on purpose. The demo runs for a few seconds, so no token
 * comes back while it runs, and every count it prints is exact on every machine. A real
 * shop would refill far more often; the lesson does not change.
 */
public final class SearchLimit {

    public static final int TOKENS = 10;
    public static final Duration REFILL_EVERY = Duration.ofHours(1);

    private SearchLimit() {
    }

    /** What Bucket4j calls the configuration of a bucket: its size and how it refills. */
    public static BucketConfiguration configuration() {
        Bandwidth tenAnHour = Bandwidth.builder()
                .capacity(TOKENS)
                .refillIntervally(TOKENS, REFILL_EVERY)
                .build();
        return BucketConfiguration.builder().addLimit(tenAnHour).build();
    }

    /** A bucket that lives in this program's memory and nowhere else. */
    public static Bucket inMemoryBucket() {
        return Bucket.builder().addLimit(configuration().getBandwidths()[0]).build();
    }

    /** The Redis key that holds one client's bucket. */
    public static String keyFor(String clientId) {
        return "search-limit:" + clientId;
    }
}
