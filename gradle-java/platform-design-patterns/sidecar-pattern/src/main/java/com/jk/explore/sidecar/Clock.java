package com.jk.explore.sidecar;

/**
 * A clock that is moved by hand rather than by the passage of time.
 *
 * <p>Nothing in this project sleeps. When a retry waits two hundred milliseconds, the
 * waiting is recorded by adding two hundred to a number. That is why the whole demo
 * finishes instantly and prints the same figures on a fast laptop and a slow one, and it
 * is also why every timing quoted in the documents can be asserted by a test.
 *
 * <p>Each service gets its own clock, and all of them start at zero at the moment the
 * payment gateway starts misbehaving. So "now" here always means "milliseconds since the
 * trouble began", which is the only time reference the story needs.
 */
public final class Clock {

    private long millis;

    public long now() {
        return millis;
    }

    /** Records a wait without performing one. */
    public void waitFor(long forMillis) {
        millis += forMillis;
    }

    public void reset() {
        millis = 0;
    }
}
