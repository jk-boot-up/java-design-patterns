package com.jk.explore.queryobject;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: SQL glued from strings, a query object, the same query in memory, safe and reusable, and the bill.
 */
public final class QueryObjectDemo {

    static final List<Product> TABLE = List.of(
            new Product("steel kettle", "kitchen", 3000, 4),
            new Product("glass teapot", "kitchen", 2500, 0),
            new Product("tea towel", "kitchen", 600, 12),
            new Product("O'Brien's mug", "kitchen", 900, 3),
            new Product("desk lamp", "home", 2200, 5));

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. The search page glues SQL together from strings.");
        out.add("  kitchen under £30: " + StringSql.build("kitchen", 3000L, null));
        out.add("  any category under £30: " + StringSql.build(null, 3000L, null));
        out.add("  name contains O'Brien: " + StringSql.build("kitchen", null, "O'Brien"));
        out.add("  the second is broken SQL; the third lets the customer's quote end the string");

        out.add("");
        out.add("TWO. A query object, built from criteria.");
        ProductQuery cheapKitchen = ProductQuery.all().and(Criterion.category("kitchen"))
                .and(Criterion.maxPrice(3000)).and(Criterion.inStock());
        out.add("  SQL:    " + cheapKitchen.toSql());
        out.add("  values: " + cheapKitchen.params());
        ProductQuery anyCheap = ProductQuery.all().and(Criterion.maxPrice(3000));
        out.add("  any category under £30: " + anyCheap.toSql());

        out.add("");
        out.add("THREE. The same query runs in memory, for tests.");
        cheapKitchen.runOn(TABLE).forEach(p -> out.add("  found " + p.name() + ", " + pounds(p.pricePence())));
        out.add("  the glass teapot is out of stock, the lamp is not kitchen: both left out");

        out.add("");
        out.add("FOUR. Safe with any text, and reusable.");
        ProductQuery obrien = cheapKitchen.and(Criterion.nameContains("O'Brien"));
        out.add("  SQL:    " + obrien.toSql());
        out.add("  values: " + obrien.params());
        out.add("  the quote travels as a value, never as SQL; found " + obrien.runOn(TABLE).size() + " product");
        out.add("  the saved \"cheap kitchen\" query was reused, not changed: still " + cheapKitchen.params().size() + " values");

        out.add("");
        out.add("FIVE. The bill: a small query language of your own.");
        out.add("  only the criteria you wrote exist: no OR, no joins, no sorting yet");
        out.add("  and each criterion says the same thing twice, in SQL and in Java, which must agree");
        return out;
    }

    static String pounds(long pence) {
        return String.format("£%d.%02d", pence / 100, pence % 100);
    }

    private QueryObjectDemo() {
    }
}
