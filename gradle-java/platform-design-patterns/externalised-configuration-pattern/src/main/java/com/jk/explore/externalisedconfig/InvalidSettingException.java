package com.jk.explore.externalisedconfig;

/**
 * Thrown when a configured value cannot be used — either it is not a number at
 * all, or it is a number the shop has no business accepting.
 *
 * <p>The message is written to be read by whoever is on call at the time, so it
 * always names the key, quotes the offending text, and says what was expected.
 * "Invalid configuration" on its own is a cruelty at three in the morning.
 *
 * <p>Whether this exception ever escapes as far as a customer is the whole
 * difference between the two settings readers in this project.
 * {@link TrustingSettings} lets it out, and every checkout fails.
 * {@link GuardedSettings} catches it at the boundary, keeps the last good value,
 * and the shop carries on selling while somebody fixes the typo.
 */
public class InvalidSettingException extends RuntimeException {

    private final String key;
    private final String offendingValue;

    public InvalidSettingException(String key, String offendingValue, String expected) {
        super("setting '" + key + "' has value \"" + offendingValue + "\" — " + expected);
        this.key = key;
        this.offendingValue = offendingValue;
    }

    /** The setting that was wrong. */
    public String key() {
        return key;
    }

    /** The text that could not be used, exactly as it was configured. */
    public String offendingValue() {
        return offendingValue;
    }
}
