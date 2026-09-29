package com.jk.explore.translator;

/**
 * The warehouse. The old version parsed every format itself; the new one only ever sees OrderMessage.
 */
public final class Warehouse {

    /** Without the pattern: every format's parsing lives inside the warehouse. */
    public static String pickOld(String raw) {
        if (raw.startsWith("order=")) {
            return "pick " + raw.split(";")[1].substring(4);
        } else if (raw.matches("A-\\d+,.*")) {
            return "pick " + raw.split(",")[1];
        } else if (raw.startsWith("{")) {
            return "pick " + Translators.json(raw, "item");
        }
        throw new IllegalArgumentException("warehouse cannot read this order");
    }

    public static String pick(OrderMessage order) {
        return "pick " + order.quantity() + " x " + order.sku() + " for " + order.orderId();
    }

    private Warehouse() {
    }
}
