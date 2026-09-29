package com.jk.explore.translator;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: the warehouse reads every format, translators, the normalizer, a new marketplace, and the bill.
 */
public final class MessageTranslatorDemo {

    static final String WEB = "order=W-1;sku=KETTLE-1;qty=1;price=30.00";
    static final String CSV = "A-77,MUG-1,2,1600";
    static final String JSON = "{\"id\":\"B-9\",\"item\":\"TEAPOT-1\",\"count\":1,\"amount\":\"£25.00\",\"gift_note\":\"Happy birthday, Mum\"}";
    static final String XML = "<order id=\"C-5\"><sku>KETTLE-1</sku><qty>1</qty><pence>3000</pence></order>";

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. The warehouse reads every marketplace's format itself.");
        for (String raw : List.of(WEB, CSV, JSON)) {
            out.add("  " + Warehouse.pickOld(raw));
        }
        try {
            Warehouse.pickOld(XML);
        } catch (IllegalArgumentException e) {
            out.add("  a new marketplace sends XML: " + e.getMessage());
        }
        out.add("  three formats' parsing lives inside the warehouse; every new one means changing it");

        out.add("");
        out.add("TWO. A translator per format, all producing one canonical order.");
        out.add("  web form   -> " + Translators.WEB.translate(WEB));
        out.add("  CSV        -> " + Translators.MARKET_A.translate(CSV));
        out.add("  JSON       -> " + Translators.MARKET_B.translate(JSON));

        out.add("");
        out.add("THREE. A normalizer recognises the format and picks the translator.");
        Normalizer normalizer = Normalizer.standard();
        for (String raw : List.of(CSV, JSON, WEB)) {
            OrderMessage m = normalizer.normalize(raw);
            out.add("  " + normalizer.formatOf(raw) + ": " + Warehouse.pick(m));
        }
        out.add("  the warehouse only ever sees OrderMessage");

        out.add("");
        out.add("FOUR. A new marketplace: one translator, one rule.");
        normalizer.route("marketplace C (XML)", raw -> raw.startsWith("<order"), Translators.MARKET_C);
        out.add("  " + normalizer.formatOf(XML) + ": " + Warehouse.pick(normalizer.normalize(XML)));
        out.add("  the warehouse was not changed");

        out.add("");
        out.add("FIVE. The bill: what the canonical order has no room for is lost.");
        out.add("  marketplace B's gift note: \"" + Translators.json(JSON, "gift_note") + "\"");
        out.add("  after translation: " + normalizer.normalize(JSON) + ", no gift note");
        out.add("  every field someone needs must be added to the canonical order, and to every translator");
        return out;
    }

    private MessageTranslatorDemo() {
    }
}
