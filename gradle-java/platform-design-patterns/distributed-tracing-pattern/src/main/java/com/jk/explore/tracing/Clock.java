package com.jk.explore.tracing;

/**
 * Where the time comes from.
 *
 * <p>A tracing demo that used the real wall clock would print different numbers
 * on every run, and the whole argument of this project is about specific
 * numbers — nine hundred milliseconds for the page, four hundred of them in one
 * service. Those have to be the same every time, or the tests cannot check them
 * and the narration cannot quote them.
 *
 * <p>So work is not really performed here. It is <em>declared</em>: a service
 * says "this took a hundred and twenty milliseconds" and the clock moves
 * forward by that much. Everything downstream — the spans, the waterfall, the
 * percentages — is then computed from real arithmetic on those declared
 * durations, exactly as it would be on real ones.
 */
public interface Clock {

    /** Milliseconds since the request started. */
    long now();

    /**
     * A clock that only moves when it is told to.
     *
     * <p>Deliberately not thread-safe in the way a production clock would be,
     * because one of the lessons in this project is what happens when work
     * moves to another thread, and a clock that quietly papered over that
     * would be hiding the thing being taught.
     */
    final class Scripted implements Clock {

        private long millis;

        @Override
        public long now() {
            return millis;
        }

        /**
         * Move time forward, as though work had been done.
         *
         * @param duration how long the work took, in milliseconds
         * @return the instant the work finished
         */
        public long advance(long duration) {
            if (duration < 0) {
                throw new IllegalArgumentException("work cannot take negative time: " + duration);
            }
            millis += duration;
            return millis;
        }
    }
}
