package com.jk.explore.externalisedconfig;

/**
 * Reads one setting and says what value is in force.
 *
 * <p>This is the seam between the program and the outside world, and it is the
 * only place in the project that knows a configuration source exists. Everything
 * downstream — {@link ConfiguredCheckout} included — asks for money and gets
 * money.
 *
 * <p>There are two implementations, and swapping one for the other changes
 * nothing about the shop on a good day and everything about the shop on a bad
 * one. {@link TrustingSettings} takes the source at its word.
 * {@link GuardedSettings} checks it against the setting's declared range, keeps
 * the last value that passed, and refuses to let a typo out of the door. The
 * demo runs both against the same two bad values so you can watch the
 * difference rather than take it on trust.
 */
public interface SettingsReader {

    /** The value in force for this setting, and where it came from. */
    SettingValue money(MoneySetting setting);

    /** How this reader would describe itself in a report. */
    String describe();
}
