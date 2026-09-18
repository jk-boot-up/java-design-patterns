package com.jk.explore.externalisedconfig;

/**
 * A value the program is about to act on, together with where it came from.
 *
 * <p>Carrying the origin alongside the value costs one field and saves entire
 * afternoons. Once a number can come from a config server, from a cached last
 * good value, or from a default baked into the build, "the threshold is
 * thirty-five" stops being a complete answer to anything. "The threshold is
 * thirty-five, from the config server" and "the threshold is fifty, from the
 * default compiled into the code, because the server did not answer" are
 * different situations that look identical on a checkout page.
 *
 * @param amount the value in force
 * @param origin where it came from, in plain words fit to print
 */
public record SettingValue(Money amount, String origin) {
}
