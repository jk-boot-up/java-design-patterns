package com.jk.explore.queryobject;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

/**
 * The pattern: a search held as an object made of criteria, which can become safe SQL or run over a list in memory.
 *
 * <p>Adding a criterion returns a new query, so a saved search can be the
 * starting point for many others without being changed.
 */
public final class ProductQuery {

    private final List<Criterion> criteria;

    private ProductQuery(List<Criterion> criteria) {
        this.criteria = List.copyOf(criteria);
    }

    public static ProductQuery all() {
        return new ProductQuery(List.of());
    }

    public ProductQuery and(Criterion c) {
        List<Criterion> next = new ArrayList<>(criteria);
        next.add(c);
        return new ProductQuery(next);
    }

    public String toSql() {
        String where = criteria.stream().map(Criterion::sql).collect(Collectors.joining(" AND "));
        return "SELECT * FROM product" + (where.isEmpty() ? "" : " WHERE " + where);
    }

    public List<Object> params() {
        List<Object> all = new ArrayList<>();
        criteria.forEach(c -> all.addAll(c.params()));
        return all;
    }

    public List<Product> runOn(List<Product> table) {
        return table.stream().filter(p -> criteria.stream().allMatch(c -> c.test(p))).toList();
    }
}
