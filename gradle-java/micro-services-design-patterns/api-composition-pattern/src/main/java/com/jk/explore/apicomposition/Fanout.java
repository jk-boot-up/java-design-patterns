package com.jk.explore.apicomposition;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Supplier;

/**
 * Several calls that all leave at once, and a wait for the slowest of them.
 *
 * This is the entire mechanical content of API Composition. Sequential calls cost the
 * sum of their latencies; parallel calls cost the maximum. Thirty plus sixty plus a
 * hundred and twenty is two hundred and ten milliseconds of shopper staring at a
 * spinner, and the same three calls made together cost a hundred and twenty.
 *
 * <p>The second job this class does is quieter and matters just as much: a branch that
 * throws does not bring down the fan-out. The failure is caught and parked on the
 * branch, and the composer decides afterwards, one branch at a time, whether that
 * particular absence is fatal or merely a gap on the page.
 *
 * <p>In a real service this would be a virtual thread per branch, or
 * {@code CompletableFuture.allOf}, and a timeout on each one. Here it is a loop and a
 * clock that gets wound back between branches, which produces the same timeline
 * without needing threads to reason about. Nothing in this project sleeps.
 */
public final class Fanout {

    /** One call in flight: a name, the work, and whatever came back — or did not. */
    public static final class Branch<T> {

        private final String name;
        private final Supplier<T> call;
        private T value;
        private RuntimeException failure;

        private Branch(String name, Supplier<T> call) {
            this.name = name;
            this.call = call;
        }

        private void run() {
            try {
                value = call.get();
            } catch (RuntimeException thrown) {
                failure = thrown;
            }
        }

        public String name() {
            return name;
        }

        public boolean failed() {
            return failure != null;
        }

        /** The answer, or the branch's failure rethrown. For data the page needs. */
        public T value() {
            if (failure != null) {
                throw failure;
            }
            return value;
        }

        /** The answer, or {@code fallback}. For data the page can do without. */
        public T valueOr(T fallback) {
            return failure == null ? value : fallback;
        }
    }

    private final SimulatedClock clock;
    private final CallLog log;
    private final List<Branch<?>> branches = new ArrayList<>();

    public Fanout(SimulatedClock clock, CallLog log) {
        this.clock = clock;
        this.log = log;
    }

    /** Adds a call to the fan-out. Nothing happens until {@link #awaitAll()}. */
    public <T> Branch<T> add(String name, Supplier<T> call) {
        Branch<T> branch = new Branch<>(name, call);
        branches.add(branch);
        return branch;
    }

    /** Sends every branch at once and waits for the slowest to come back. */
    public void awaitAll() {
        long leftAt = clock.millis();
        long slowestBackAt = leftAt;

        for (Branch<?> branch : branches) {
            clock.moveTo(leftAt);
            branch.run();
            slowestBackAt = Math.max(slowestBackAt, clock.millis());
        }
        clock.moveTo(slowestBackAt);

        long failures = branches.stream().filter(Branch::failed).count();
        log.note("Composer", "GATHERED", branches.size() + " call(s) in "
                + (slowestBackAt - leftAt) + "ms, " + failures + " failed");
    }
}
