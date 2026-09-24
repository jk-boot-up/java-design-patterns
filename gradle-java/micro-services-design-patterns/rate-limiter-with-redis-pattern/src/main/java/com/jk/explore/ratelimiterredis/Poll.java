package com.jk.explore.ratelimiterredis;

import java.time.Duration;
import java.util.function.BooleanSupplier;

/**
 * Waits for something to become true, and gives up loudly if it never does.
 *
 * <p>Real infrastructure takes a moment to catch up, and the temptation is to wait a fixed
 * number of seconds and hope. That makes a slow machine fail and a fast machine waste time.
 * Instead every wait in this project asks a question over and over until the answer is yes,
 * and fails with the question in the message if the time runs out.
 */
public final class Poll {

    private static final Duration LIMIT = Duration.ofSeconds(60);
    private static final long STEP_MILLIS = 50;

    private Poll() {
    }

    public static void until(String whatWeAreWaitingFor, BooleanSupplier condition) {
        until(whatWeAreWaitingFor, LIMIT, condition);
    }

    public static void until(String whatWeAreWaitingFor, Duration limit, BooleanSupplier condition) {
        long deadline = System.nanoTime() + limit.toNanos();
        while (System.nanoTime() < deadline) {
            if (quietly(condition)) {
                return;
            }
            pause();
        }
        throw new IllegalStateException("gave up waiting for: " + whatWeAreWaitingFor);
    }

    private static boolean quietly(BooleanSupplier condition) {
        try {
            return condition.getAsBoolean();
        } catch (RuntimeException e) {
            return false;
        }
    }

    private static void pause() {
        try {
            Thread.sleep(STEP_MILLIS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException("interrupted while waiting");
        }
    }
}
