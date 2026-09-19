package com.jk.explore.pipesfilters;

import java.util.List;
import java.util.Optional;

/** The order-import steps, each a small filter over its own types. */
public final class Shop {

    private Shop() {
    }

    public record Parsed(String customer, String sku, int quantity) {
    }

    public record Priced(String customer, String sku, int quantity, long netPence) {
    }

    public record Taxed(String customer, String sku, int quantity, long grossPence) {
    }

    public static Filter<String, Parsed> parse() {
        return new Filter<>() {
            public String name() {
                return "parse";
            }

            public Optional<Parsed> apply(String line, List<String> rejects) {
                String[] p = line.split(",");
                if (p.length != 3) {
                    rejects.add("parse: '" + line + "' does not have three fields");
                    return Optional.empty();
                }
                try {
                    return Optional.of(new Parsed(p[0].trim(), p[1].trim(), Integer.parseInt(p[2].trim())));
                } catch (NumberFormatException e) {
                    rejects.add("parse: quantity '" + p[2].trim() + "' is not a number");
                    return Optional.empty();
                }
            }
        };
    }

    public static Filter<Parsed, Parsed> validate() {
        return new Filter<>() {
            public String name() {
                return "validate";
            }

            public Optional<Parsed> apply(Parsed p, List<String> rejects) {
                if (p.quantity() < 1 || p.quantity() > 10) {
                    rejects.add("validate: " + p.customer() + " asked for " + p.quantity() + " of " + p.sku());
                    return Optional.empty();
                }
                return Optional.of(p);
            }
        };
    }

    public static Filter<Parsed, Priced> price() {
        return Filter.of("price", p -> new Priced(p.customer(), p.sku(), p.quantity(), (p.sku().startsWith("ESP") ? 30000L : 800L) * p.quantity()));
    }

    public static Filter<Priced, Taxed> ukTax() {
        return Filter.of("uk-tax", p -> new Taxed(p.customer(), p.sku(), p.quantity(), p.netPence() + p.netPence() / 5));
    }

    public static Filter<Priced, Taxed> euTax() {
        return Filter.of("eu-tax", p -> new Taxed(p.customer(), p.sku(), p.quantity(), p.netPence() + p.netPence() * 21 / 100));
    }

    public static Filter<Taxed, String> format() {
        return Filter.of("format", t -> String.format("%s: %d x %s = £%d.%02d", t.customer(), t.quantity(), t.sku(), t.grossPence() / 100, t.grossPence() % 100));
    }

    public static final List<String> LINES = List.of("ada, MUG-BLUE, 2", "ben, ESP-001, 1", "cy, MUG-BLUE, twelve", "di, MUG-BLUE, 50", "ed, TEA-050", "fay, TEA-050, 3");
}
