package com.jk.explore.externalisedconfig;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * One recorded alteration to one setting.
 *
 * <p>Five facts, and every one of them earns its place. <em>Which</em> key,
 * <em>what</em> it was before, <em>what</em> it became, <em>when</em>, and
 * <em>who</em>. Drop any one of them and the record stops being able to answer
 * the question you will actually be asked, which is never "what is the threshold
 * now" — you can read that off the server — but "what was it at nine o'clock on
 * Saturday, and whose change made it that".
 *
 * <p>The {@code was} value is the one people leave out, and it is the one that
 * makes a rollback possible without guesswork. If the log says the threshold
 * went from {@code "50"} to {@code "-1"}, putting it back is not a judgement
 * call. If it only says the threshold is now {@code "-1"}, somebody has to
 * remember what it used to be, at speed, while the shop gives away delivery.
 *
 * @param sequence the order this change happened in, counting from one
 * @param at when it took effect
 * @param key the setting that changed
 * @param was the previous value as text, or {@code "(not set)"} if there was none
 * @param now the new value as text
 * @param who the person or system that made the change
 */
public record ConfigChange(int sequence,
                           LocalDateTime at,
                           String key,
                           String was,
                           String now,
                           String who) {

    /** Used when a key is being set for the very first time. */
    public static final String NOT_SET = "(not set)";

    private static final DateTimeFormatter STAMP =
            DateTimeFormatter.ofPattern("EEE dd MMM HH:mm:ss");

    /** One line for the audit report, wide enough to line up in a column. */
    public String asLine() {
        return String.format("#%d  %s  %-18s %-8s -> %-8s  by %s",
                sequence, STAMP.format(at), key, was, now, who);
    }
}
