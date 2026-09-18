package com.jk.explore.sidecarjavaproxy;

import java.util.ArrayList;
import java.util.List;

/**
 * Every attempt the payment provider received, in the order it received them, with the
 * millisecond each one arrived.
 *
 * <p>The log is kept by the provider rather than by the proxies, and the timestamps are
 * taken at the far end. That is what makes this project's central comparison something
 * you can check rather than something you are told: a proxy claiming it spaced its
 * retries out is a claim, and the provider's own arrival times are evidence.
 */
public final class CallLog {

    /** One attempt, as the provider saw it. */
    public record Attempt(String service, String orderRef, long atMillis, String outcome) {
    }

    private final List<Attempt> attempts = new ArrayList<>();

    public void record(String service, String orderRef, long atMillis, String outcome) {
        attempts.add(new Attempt(service, orderRef, atMillis, outcome));
    }

    public List<Attempt> attempts() {
        return List.copyOf(attempts);
    }

    public int total() {
        return attempts.size();
    }

    public int countOf(String outcome) {
        return (int) attempts.stream().filter(a -> a.outcome().equals(outcome)).count();
    }

    /**
     * The millisecond between the first attempt and the last.
     *
     * <p>This single number is the whole argument of the project. Three attempts that
     * span three milliseconds and three attempts that span six hundred cost the provider
     * exactly the same and buy the shop completely different outcomes.
     */
    public long spanMillis() {
        if (attempts.isEmpty()) {
            return 0;
        }
        return attempts.get(attempts.size() - 1).atMillis() - attempts.get(0).atMillis();
    }

    public void clear() {
        attempts.clear();
    }
}
