package com.jk.explore.externalisedconfig;

import java.util.Optional;

/**
 * The declaration of one money setting: its name, its default, and the range of
 * values the shop is prepared to believe.
 *
 * <p>This little record is the replacement for the compiler. When the threshold
 * was a constant in the source, three things guarded it for free. The compiler
 * refused to let it be the word "fifty". The type system refused to let it be
 * anything but money. And a reviewer would have queried minus one pound out of
 * ordinary human surprise. Move the value outside the program and all three
 * guards stay behind — the value now arrives as text, at runtime, unread by
 * anybody.
 *
 * <p>So you write them down instead. A name, so the log can say which setting
 * went wrong. A fallback, so the shop can start when the source is unreachable.
 * And a lowest and highest value, because "how wrong can this legitimately be"
 * is a question with a real answer, and answering it here is what stops minus
 * one pound reaching a customer.
 *
 * <p>This is the idea behind typed configuration in every real framework —
 * Spring's {@code @ConfigurationProperties} with validation annotations,
 * a JSON schema in front of a config server — reduced to the smallest thing that
 * still teaches it.
 *
 * @param key the name the value is stored under
 * @param fallback the value compiled into the program, used when nothing else works
 * @param lowest the smallest value the shop will accept
 * @param highest the largest value the shop will accept
 */
public record MoneySetting(String key, Money fallback, Money lowest, Money highest) {

    /**
     * Turns configured text into money, or explains why it cannot.
     *
     * <p>Two ways to fail, and they are worth keeping separate in your head
     * because they fail differently in production. Text that is not a number at
     * all — {@code "fifty"} — fails loudly the first time anything reads it. A
     * number outside the sensible range — {@code "-1"} — does not fail at all
     * unless somebody asks the question this method asks. It simply works, and
     * gives delivery away.
     *
     * @throws InvalidSettingException if the text is not a number, or is out of range
     */
    public Money read(String raw) {
        Optional<Money> parsed = Money.parse(raw);
        if (parsed.isEmpty()) {
            throw new InvalidSettingException(key, raw,
                    "expected an amount of money such as \"35\" or \"4.99\"");
        }
        Money value = parsed.get();
        if (value.compareTo(lowest) < 0 || value.compareTo(highest) > 0) {
            throw new InvalidSettingException(key, raw,
                    "expected between " + lowest + " and " + highest);
        }
        return value;
    }

    /** True when this text would be accepted, without throwing to find out. */
    public boolean accepts(String raw) {
        try {
            read(raw);
            return true;
        } catch (InvalidSettingException rejected) {
            return false;
        }
    }

    /** The range, in words, for the schema printed by the demo. */
    public String describeRange() {
        return lowest + " to " + highest;
    }
}
