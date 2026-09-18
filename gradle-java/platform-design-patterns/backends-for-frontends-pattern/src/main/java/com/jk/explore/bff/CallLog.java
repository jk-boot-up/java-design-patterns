package com.jk.explore.bff;

import java.util.ArrayList;
import java.util.List;

/**
 * Every call made while one screen was being built, in the order it happened, and
 * where it was made from.
 *
 * <p>Two columns matter and they are easy to confuse. A call from the phone to the
 * shop crosses the customer's mobile network, and on a bad connection that is a tenth
 * of a second before anything has been computed. A call from a backend to another
 * backend happens inside the data centre, on a network that is close to free. The
 * pattern does not remove work; it moves calls from the first column to the second,
 * and the only way to argue that honestly is to count them separately.
 */
public final class CallLog {

    /** Where a call was made from. */
    public enum Origin {
        /** Across the customer's own connection. Slow, metered, and unreliable. */
        DEVICE,
        /** Inside the data centre, between our own processes. Fast and free. */
        INTERNAL
    }

    public record Call(Origin origin, String target) {
    }

    private final List<Call> calls = new ArrayList<>();

    public void record(Origin origin, String target) {
        calls.add(new Call(origin, target));
    }

    public List<Call> calls() {
        return List.copyOf(calls);
    }

    public int countFrom(Origin origin) {
        return (int) calls.stream().filter(call -> call.origin() == origin).count();
    }

    public List<String> targetsFrom(Origin origin) {
        return calls.stream().filter(call -> call.origin() == origin).map(Call::target).toList();
    }

    public void clear() {
        calls.clear();
    }
}
