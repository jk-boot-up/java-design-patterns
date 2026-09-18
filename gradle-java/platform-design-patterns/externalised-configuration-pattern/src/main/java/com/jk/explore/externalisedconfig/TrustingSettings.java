package com.jk.explore.externalisedconfig;

import java.util.Optional;

/**
 * The settings reader you write first: it externalises the value, and stops
 * there.
 *
 * <p>This class does the good half of the pattern and none of the careful half.
 * It reads the key from the source on every call, so a change is live on the next
 * order with no rebuild. It falls back to the setting's default when the key is
 * missing or the source is unreachable, so the shop starts and keeps running
 * through an outage. Those two behaviours are the reason anyone externalises
 * configuration, and they are genuinely worth having.
 *
 * <p>What it does not do is ask whether the value makes sense. It parses the
 * text and uses whatever comes out, which means:
 *
 * <ul>
 *   <li>{@code "-1"} becomes minus one pound, every basket clears a negative
 *       threshold, and the shop gives delivery away to everybody — quietly,
 *       with no error anywhere, until somebody looks at the margin.</li>
 *   <li>{@code "fifty"} is not a number, so the read throws, and because
 *       nothing here catches it the exception travels straight out through
 *       checkout. Every customer sees a failure.</li>
 * </ul>
 *
 * <p>Both of those reach the running shop in four seconds, from a text box, with
 * no compiler, no code review and no test suite in the way. That is the bill for
 * this pattern, and this class is here so you can see it arrive rather than be
 * warned about it. {@link GuardedSettings} is the same class with the bill paid.
 */
public final class TrustingSettings implements SettingsReader {

    private final ConfigSource source;

    public TrustingSettings(ConfigSource source) {
        this.source = source;
    }

    @Override
    public SettingValue money(MoneySetting setting) {
        Optional<String> raw;
        try {
            raw = source.lookup(setting.key());
        } catch (ConfigSourceUnavailableException unreachable) {
            return new SettingValue(setting.fallback(),
                    "the default compiled into the code, because " + source.name()
                            + " could not be reached");
        }
        if (raw.isEmpty()) {
            return new SettingValue(setting.fallback(),
                    "the default compiled into the code, because " + source.name()
                            + " has no value for " + setting.key());
        }
        // No range check. Whatever the text parses to is what the shop will use,
        // and if it does not parse at all this line throws into the caller.
        Money value = Money.parse(raw.get())
                .orElseThrow(() -> new InvalidSettingException(setting.key(), raw.get(),
                        "expected an amount of money such as \"35\" or \"4.99\""));
        return new SettingValue(value, source.name());
    }

    @Override
    public String describe() {
        return "TrustingSettings, reading " + source.name() + " with no validation";
    }
}
