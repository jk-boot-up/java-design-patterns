package com.jk.explore.externalisedconfig;

import java.util.Optional;

/**
 * Somewhere outside the program that values can be read from.
 *
 * <p>In a real shop this is a configuration server, a mounted file, a set of
 * environment variables, or a row in a table. Here it is {@link ConfigServer},
 * an ordinary map with a clock and an audit trail bolted on, because the lesson
 * is not about how any particular one of those is wired up.
 *
 * <p>Two things about the shape of this interface are worth saying out loud.
 *
 * <p>First, {@link #lookup(String)} returns an {@link Optional}. A configuration
 * source not having a value for a key is not an error — it is Tuesday. The key
 * has not been set yet, or it was deliberately removed, and the program is
 * expected to carry on with its own default. A source that threw on a missing
 * key would make every caller write a try-catch around the normal case.
 *
 * <p>Second, {@code lookup} <em>is</em> allowed to throw, but only for one
 * reason: the source could not be reached at all. That is a genuinely different
 * situation from "there is no value", and conflating the two is how shops end up
 * silently reverting to defaults during a network incident and only finding out
 * from the sales figures. See {@link ConfigSourceUnavailableException}.
 */
public interface ConfigSource {

    /**
     * The value for this key as text, or empty if the source has none.
     *
     * @throws ConfigSourceUnavailableException if the source cannot be reached
     */
    Optional<String> lookup(String key);

    /** What to call this source when explaining where a value came from. */
    String name();
}
