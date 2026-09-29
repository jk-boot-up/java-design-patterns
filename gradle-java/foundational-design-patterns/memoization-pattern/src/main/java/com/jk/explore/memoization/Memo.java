package com.jk.explore.memoization;

import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;

/**
 * The pattern as a reusable wrapper: remembers the answer for every argument it has seen.
 *
 * <p>Only correct for functions whose answer depends on nothing but the
 * argument. It never forgets, so it grows with every new argument.
 */
public final class Memo<A, R> implements Function<A, R> {

    private final Function<A, R> slow;
    private final Map<A, R> answers = new HashMap<>();
    private int slowCalls;

    public Memo(Function<A, R> slow) {
        this.slow = slow;
    }

    @Override
    public R apply(A argument) {
        return answers.computeIfAbsent(argument, a -> {
            slowCalls++;
            return slow.apply(a);
        });
    }

    public int slowCalls() {
        return slowCalls;
    }

    public int size() {
        return answers.size();
    }
}
