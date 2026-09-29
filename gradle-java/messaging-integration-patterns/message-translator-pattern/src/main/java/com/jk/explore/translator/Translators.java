package com.jk.explore.translator;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * The pattern: one small translator per incoming format, each turning its format into the canonical OrderMessage.
 */
public final class Translators {

    public interface Translator {
        OrderMessage translate(String raw);
    }

    /** The shop's own web form: "order=W-1;sku=KETTLE-1;qty=1;price=30.00". */
    public static final Translator WEB = raw -> {
        String[] f = raw.split(";");
        return new OrderMessage(value(f[0]), value(f[1]), Integer.parseInt(value(f[2])),
                Math.round(Double.parseDouble(value(f[3])) * 100));
    };

    /** Marketplace A sends CSV: "A-77,MUG-1,2,1600" (total in pence). */
    public static final Translator MARKET_A = raw -> {
        String[] f = raw.split(",");
        return new OrderMessage(f[0], f[1], Integer.parseInt(f[2]), Long.parseLong(f[3]));
    };

    /** Marketplace B sends JSON with its own names: id, item, count, amount (£) and gift_note. */
    public static final Translator MARKET_B = raw -> new OrderMessage(
            json(raw, "id"), json(raw, "item"), Integer.parseInt(json(raw, "count")),
            Math.round(Double.parseDouble(json(raw, "amount").replace("£", "")) * 100));

    /** Marketplace C, added later, sends XML. */
    public static final Translator MARKET_C = raw -> new OrderMessage(
            match(raw, "id=\"([^\"]+)\""), match(raw, "<sku>([^<]+)</sku>"),
            Integer.parseInt(match(raw, "<qty>(\\d+)</qty>")), Long.parseLong(match(raw, "<pence>(\\d+)</pence>")));

    private static String value(String kv) {
        return kv.substring(kv.indexOf('=') + 1);
    }

    static String json(String raw, String key) {
        Matcher m = Pattern.compile("\"" + key + "\"\\s*:\\s*(?:\"([^\"]*)\"|([^,}]+))").matcher(raw);
        if (!m.find()) {
            return null;
        }
        return m.group(1) != null ? m.group(1) : m.group(2).trim();
    }

    private static String match(String raw, String regex) {
        Matcher m = Pattern.compile(regex).matcher(raw);
        if (!m.find()) {
            throw new IllegalArgumentException("missing " + regex);
        }
        return m.group(1);
    }

    private Translators() {
    }
}
