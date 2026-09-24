package com.jk.explore.ratelimiterredis;

import io.lettuce.core.ScriptOutputType;
import io.lettuce.core.api.sync.RedisCommands;

/**
 * A count of tokens left, kept in one Redis key, with the reading and the writing done as
 * two separate steps so the demo can put another server's steps in between them.
 *
 * <p>This is what most people write first: read the number, check it, write it back one
 * lower. It shares the count, and it still lets two servers spend the same token.
 */
public class PlainCounter {

    /**
     * Change the value only if it is still what the caller read. Redis runs a script like
     * this in one step, with nothing from any other connection in between.
     */
    private static final String SWAP_IF_UNCHANGED =
            "if redis.call('GET', KEYS[1]) == ARGV[1] then "
            + "redis.call('SET', KEYS[1], ARGV[2]) return 1 "
            + "else return 0 end";

    private final RedisCommands<String, String> redis;
    private final String key;

    public PlainCounter(Redis redis, String clientId) {
        this.redis = redis.look();
        this.key = "search-count:" + clientId;
    }

    public void fill(int tokens) {
        redis.set(key, Integer.toString(tokens));
    }

    public int read() {
        String value = redis.get(key);
        return value == null ? 0 : Integer.parseInt(value);
    }

    /** Write the new value, whatever is there now. */
    public void writeBlindly(int tokens) {
        redis.set(key, Integer.toString(tokens));
    }

    /** Write the new value only if the key still holds what was read. True if it did. */
    public boolean writeIfStill(int read, int tokens) {
        Long swapped = redis.eval(SWAP_IF_UNCHANGED, ScriptOutputType.INTEGER,
                new String[]{key}, Integer.toString(read), Integer.toString(tokens));
        return swapped != null && swapped == 1L;
    }
}
