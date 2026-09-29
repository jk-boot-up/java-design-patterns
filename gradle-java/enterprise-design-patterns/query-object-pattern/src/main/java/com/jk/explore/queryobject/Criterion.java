package com.jk.explore.queryobject;

import java.util.List;

/**
 * One condition of a query. It can write itself as SQL with placeholders, and it can test a product in memory.
 */
public interface Criterion {

    String sql();

    List<Object> params();

    boolean test(Product p);

    static Criterion category(String category) {
        return of("category = ?", List.of(category), p -> p.category().equals(category));
    }

    static Criterion maxPrice(long pence) {
        return of("price_pence <= ?", List.of(pence), p -> p.pricePence() <= pence);
    }

    static Criterion inStock() {
        return of("stock > 0", List.of(), p -> p.stock() > 0);
    }

    static Criterion nameContains(String text) {
        return of("name LIKE ?", List.of("%" + text + "%"), p -> p.name().contains(text));
    }

    private static Criterion of(String sql, List<Object> params, java.util.function.Predicate<Product> test) {
        return new Criterion() {
            public String sql() {
                return sql;
            }

            public List<Object> params() {
                return params;
            }

            public boolean test(Product p) {
                return test.test(p);
            }
        };
    }
}
