package com.jk.explore.sidecar;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Every attempt the payment gateway received, in the order it received them.
 *
 * <p>This log is kept by the gateway, not by the callers. That is deliberate. A service
 * that believes it retries three times can be wrong — about its configuration, about
 * which branch shipped, about whether a library is retrying underneath it as well. The
 * only count anybody can argue with is the one taken at the far end, by the machine being
 * called, and in a real incident that count is the one the provider reads back to you
 * over the phone.
 */
public final class CallLog {

    /** One attempt, as the gateway saw it. */
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

    /** How many attempts each service made, in first-seen order. */
    public Map<String, Integer> byService() {
        Map<String, Integer> counts = new LinkedHashMap<>();
        for (Attempt attempt : attempts) {
            counts.merge(attempt.service(), 1, Integer::sum);
        }
        return counts;
    }

    public int countFor(String service) {
        return byService().getOrDefault(service, 0);
    }

    public int countOf(String outcome) {
        return (int) attempts.stream().filter(a -> a.outcome().equals(outcome)).count();
    }

    public void clear() {
        attempts.clear();
    }
}
