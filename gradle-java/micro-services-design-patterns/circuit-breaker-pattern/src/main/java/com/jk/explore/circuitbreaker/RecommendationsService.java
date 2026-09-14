package com.jk.explore.circuitbreaker;

import java.util.List;

/**
 * "You might also like…" — the least important thing on the product page.
 *
 * When it is down it does not fail quickly. It fails after the full three-second
 * timeout, which is the worst possible way for an optional feature to behave: the
 * shopper waits three seconds to be shown nothing, and for those three seconds a
 * thread that checkout needs is sitting idle waiting for an answer that is not
 * coming.
 */
public final class RecommendationsService {

    /** How long a caller waits before giving up on a service that is not answering. */
    public static final long TIMEOUT_MILLIS = 3_000;

    /** How long it takes when it is working. */
    public static final long HEALTHY_MILLIS = 20;

    private final SimulatedClock clock;
    private final CallLog log;
    private boolean down;
    private int callsReceived;

    public RecommendationsService(SimulatedClock clock, CallLog log) {
        this.clock = clock;
        this.log = log;
    }

    public RecommendationsService goDown() {
        this.down = true;
        return this;
    }

    public RecommendationsService comeBackUp() {
        this.down = false;
        return this;
    }

    /** Suggestions for a product, eventually, or a timeout three seconds from now. */
    public List<String> suggestionsFor(String sku) {
        callsReceived++;
        long startedAt = clock.millis();
        if (down) {
            clock.advance(TIMEOUT_MILLIS);
            log.record(startedAt, clock.millis(), "Recommendations", "TIMEOUT",
                    "no answer in " + TIMEOUT_MILLIS + "ms");
            throw new ServiceUnavailableException("Recommendations");
        }
        clock.advance(HEALTHY_MILLIS);
        List<String> suggestions = List.of("SKU-2001", "SKU-2002");
        log.record(startedAt, clock.millis(), "Recommendations", "OK", suggestions.toString());
        return suggestions;
    }

    /** How many calls actually arrived. The point of a breaker is to keep this low. */
    public int callsReceived() {
        return callsReceived;
    }
}
