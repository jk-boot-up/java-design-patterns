package com.jk.explore.translator;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.Predicate;

/**
 * Recognises which format an incoming message is in and sends it to the matching translator.
 */
public final class Normalizer {

    private final Map<Predicate<String>, Translators.Translator> routes = new LinkedHashMap<>();
    private final Map<Predicate<String>, String> names = new LinkedHashMap<>();

    public Normalizer route(String name, Predicate<String> looksLike, Translators.Translator translator) {
        routes.put(looksLike, translator);
        names.put(looksLike, name);
        return this;
    }

    public OrderMessage normalize(String raw) {
        for (Map.Entry<Predicate<String>, Translators.Translator> r : routes.entrySet()) {
            if (r.getKey().test(raw)) {
                return r.getValue().translate(raw);
            }
        }
        throw new IllegalArgumentException("no translator for: " + raw.substring(0, Math.min(20, raw.length())) + "...");
    }

    public String formatOf(String raw) {
        return names.entrySet().stream().filter(e -> e.getKey().test(raw)).map(Map.Entry::getValue)
                .findFirst().orElse("unknown");
    }

    public static Normalizer standard() {
        return new Normalizer()
                .route("web form", raw -> raw.startsWith("order="), Translators.WEB)
                .route("marketplace A (CSV)", raw -> raw.matches("A-\\d+,.*"), Translators.MARKET_A)
                .route("marketplace B (JSON)", raw -> raw.startsWith("{"), Translators.MARKET_B);
    }
}
