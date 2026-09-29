package com.jk.explore.translatorcamel;

import java.util.List;
import java.util.Map;

/**
 * The last step of each translator. Camel's data formats have already turned the text into
 * lists or maps; these only pick out the fields and name them the canonical way.
 */
public final class Translators {

    /** Web form: "order=W-1&sku=KETTLE-1&qty=1&price=30.00", split by Camel into a map. */
    public static OrderMessage fromWebForm(Map<String, String> form) {
        return new OrderMessage(form.get("order"), form.get("sku"), Integer.parseInt(form.get("qty")),
                Double.parseDouble(form.get("price")));
    }

    /** Marketplace A: one CSV row, unmarshalled by camel-csv: id, sku, quantity, price in pence. */
    public static OrderMessage fromCsv(List<List<String>> rows) {
        List<String> r = rows.get(0);
        return new OrderMessage(r.get(0), r.get(1), Integer.parseInt(r.get(2)), Integer.parseInt(r.get(3)) / 100.0);
    }

    /** Marketplace B: JSON with its own field names, unmarshalled by camel-jackson into a map. */
    public static OrderMessage fromJson(Map<String, Object> json) {
        return new OrderMessage((String) json.get("ref"), (String) json.get("item"),
                ((Number) json.get("count")).intValue(), ((Number) json.get("total")).doubleValue());
    }

    private Translators() {
    }
}
