package com.jk.explore.externalisedconfig;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

/**
 * The configuration source, standing in for a config server you would really
 * run as a separate process.
 *
 * <p>Underneath it is a map of text to text, which is all any configuration
 * source is. Three things are bolted on, and each one exists to make a point the
 * demo needs to make with real numbers rather than assertions.
 *
 * <p><b>A clock.</b> Every write advances it by {@link #WRITE_TAKES}. That is how
 * the demo can say that a change reaches the running shop in four seconds and
 * have the four seconds be the program's own figure rather than a claim in a
 * slide. Compare it with {@link ReleasePipeline}, which measures the same change
 * in hours.
 *
 * <p><b>A change log.</b> Every write is recorded in the {@link ChangeLog} with
 * who made it and what it displaced, because moving a value out of the source
 * code moves it out of the version history too, and something has to take that
 * job over.
 *
 * <p><b>A switch to make it unreachable.</b> {@link #goOffline(String)} makes
 * every lookup throw, so the demo can show a shop that keeps selling on its
 * compiled-in defaults while the config server is down. This is not a
 * hypothetical failure mode; it is the failure mode of this pattern.
 */
public final class ConfigServer implements ConfigSource {

    /**
     * How long a configuration change takes to be in force.
     *
     * <p>Four seconds: long enough to be honest about a write and a poll, short
     * enough to make the comparison with a release pipeline embarrassing.
     */
    public static final Duration WRITE_TAKES = Duration.ofSeconds(4);

    private final Map<String, String> values = new HashMap<>();
    private final ChangeLog changeLog;
    private LocalDateTime clock;
    private String offlineBecause;

    public ConfigServer(LocalDateTime startedAt, ChangeLog changeLog) {
        this.clock = startedAt;
        this.changeLog = changeLog;
    }

    @Override
    public Optional<String> lookup(String key) {
        if (offlineBecause != null) {
            throw new ConfigSourceUnavailableException(
                    "config server unreachable: " + offlineBecause);
        }
        return Optional.ofNullable(values.get(key));
    }

    @Override
    public String name() {
        return "the config server";
    }

    /**
     * Sets a value, advances the clock, and records who did it.
     *
     * <p>Notice what this method does not do: it does not check the value. Any
     * text at all can be written here, including {@code "-1"} and
     * {@code "fifty"}, and that is faithful to reality — a config server will
     * store whatever you type at it. Deciding whether the text makes sense is
     * the reader's job, and the difference between {@link TrustingSettings} and
     * {@link GuardedSettings} is whether anybody does it.
     *
     * @return the change as recorded, including the time it took effect
     */
    public ConfigChange set(String key, String value, String who) {
        String was = values.getOrDefault(key, ConfigChange.NOT_SET);
        clock = clock.plus(WRITE_TAKES);
        values.put(key, value);
        return changeLog.record(clock, key, was, value, who);
    }

    /**
     * Puts a key back to whatever it held before its last change.
     *
     * <p>This is the payoff of keeping the previous value in the log. A rollback
     * is the same operation as a change — one write, four seconds — rather than
     * a fresh trip through the release pipeline, and it needs nobody to remember
     * what the old number was.
     *
     * @return the recorded rollback, or empty if there is nothing to go back to
     */
    public Optional<ConfigChange> rollback(String key, String who) {
        return changeLog.valueBefore(key).map(previous -> set(key, previous, who + " (rollback)"));
    }

    /** Makes every lookup fail, as a real outage would. */
    public void goOffline(String because) {
        this.offlineBecause = because;
    }

    /** Ends the outage. */
    public void comeBackOnline() {
        this.offlineBecause = null;
    }

    /** True while the server is unreachable. */
    public boolean isOffline() {
        return offlineBecause != null;
    }

    /** The current time on the server's clock. */
    public LocalDateTime now() {
        return clock;
    }

    /**
     * Moves the clock forward to represent time passing between changes.
     *
     * <p>A real config server has a real clock and needs nothing like this. It is
     * here so the demo and the tests can put hours between two changes and have
     * the audit trail read like a weekend rather than like twenty seconds.
     */
    public void fastForwardTo(LocalDateTime moment) {
        if (moment.isAfter(clock)) {
            this.clock = moment;
        }
    }

    /** The log this server writes to. */
    public ChangeLog changeLog() {
        return changeLog;
    }
}
