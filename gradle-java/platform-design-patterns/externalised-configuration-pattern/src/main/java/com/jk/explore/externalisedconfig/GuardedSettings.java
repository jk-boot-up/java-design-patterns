package com.jk.explore.externalisedconfig;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * The settings reader you write second, after the first one has cost you a
 * morning.
 *
 * <p>It reads the same key from the same source as {@link TrustingSettings} and
 * behaves identically whenever the configured value is sensible. The difference
 * shows up only when it is not, and it takes the form of four rules.
 *
 * <p><b>Validate at the boundary.</b> Every value goes through
 * {@link MoneySetting#read(String)}, which insists the text is money and that the
 * money is in range. Nothing that fails that test gets any further into the
 * program, so the rest of the code never has to wonder.
 *
 * <p><b>Keep the last good value.</b> When a bad value arrives, the shop carries
 * on with the last one that passed. This matters more than it sounds: the
 * alternative — falling back to the compiled-in default — would quietly undo a
 * perfectly good promotion the moment somebody fat-fingered an unrelated edit.
 * Reverting to fifty pounds because a typo arrived is its own kind of wrong.
 *
 * <p><b>Fall back to the default only as a last resort.</b> If there has never
 * been a good value — the shop has only just started, and the very first thing it
 * read was rubbish — there is nothing to keep, so the default compiled into the
 * code is what keeps the shop selling.
 *
 * <p><b>Say so, loudly.</b> Every rejection is recorded in
 * {@link #rejections()}. A guard that silently swallows bad input is only half a
 * guard, because the typo is still there and the promotion still is not running.
 * Somebody has to be told. In a real shop this is a log line at error level and
 * an alert; here it is a list the demo prints.
 */
public final class GuardedSettings implements SettingsReader {

    private final ConfigSource source;
    private final Map<String, Money> lastGood = new HashMap<>();
    private final List<String> rejections = new ArrayList<>();

    public GuardedSettings(ConfigSource source) {
        this.source = source;
    }

    @Override
    public SettingValue money(MoneySetting setting) {
        Optional<String> raw;
        try {
            raw = source.lookup(setting.key());
        } catch (ConfigSourceUnavailableException unreachable) {
            return fallBack(setting, source.name() + " could not be reached");
        }
        if (raw.isEmpty()) {
            return fallBack(setting, source.name() + " has no value for " + setting.key());
        }
        try {
            Money accepted = setting.read(raw.get());
            lastGood.put(setting.key(), accepted);
            return new SettingValue(accepted, source.name());
        } catch (InvalidSettingException rejected) {
            rejections.add("REJECTED  " + rejected.getMessage());
            return fallBack(setting, "the configured value was rejected");
        }
    }

    /**
     * What to use when the configured value cannot be had: the last value that
     * passed validation if there is one, otherwise the compiled-in default.
     */
    private SettingValue fallBack(MoneySetting setting, String because) {
        Money kept = lastGood.get(setting.key());
        if (kept != null) {
            return new SettingValue(kept, "the last value that passed validation, because " + because);
        }
        return new SettingValue(setting.fallback(),
                "the default compiled into the code, because " + because);
    }

    /** Every value this reader has refused, oldest first. */
    public List<String> rejections() {
        return List.copyOf(rejections);
    }

    /** True when this reader has refused at least one value. */
    public boolean hasRejected() {
        return !rejections.isEmpty();
    }

    @Override
    public String describe() {
        return "GuardedSettings, reading " + source.name() + " and validating every value";
    }
}
