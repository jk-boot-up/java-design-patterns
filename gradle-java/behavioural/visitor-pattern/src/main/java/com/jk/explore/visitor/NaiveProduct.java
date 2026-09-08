package com.jk.explore.visitor;

import java.util.List;
import java.util.Map;

/**
 * A product that knows how to be four reports.
 *
 * <p>This is the class to read against {@link Product}. Same five fields,
 * same idea — and then four more methods, of which one is about money,
 * one is about spreadsheet file format, one is about dangerous-goods
 * paperwork, and one is about a map the caller is accumulating into.
 */
public final class NaiveProduct implements NaiveCatalogNode {

    private final String sku;
    private final String name;
    private final Money price;
    private final int stockOnHand;
    private final Restriction restriction;

    public NaiveProduct(String sku, String name, Money price, int stockOnHand) {
        this(sku, name, price, stockOnHand, Restriction.NONE);
    }

    public NaiveProduct(String sku, String name, Money price, int stockOnHand,
                        Restriction restriction) {
        this.sku = sku;
        this.name = name;
        this.price = price;
        this.stockOnHand = stockOnHand;
        this.restriction = restriction;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public Money inventoryValue() {
        return price.times(stockOnHand);
    }

    @Override
    public void countInto(Map<String, Integer> counts, String path) {
        counts.merge(path, 1, Integer::sum);
    }

    @Override
    public void appendCsvTo(StringBuilder out, String path) {
        // A product, quoting CSV fields. Correct, and written in the wrong
        // building.
        out.append(quote(path)).append(',')
                .append(quote(sku)).append(',')
                .append(quote(name)).append(",product,")
                .append(String.format("%.2f", price.asPence() / 100.0)).append(',')
                .append(stockOnHand).append(',')
                .append(quote(restriction.label()))
                .append('\n');
    }

    @Override
    public void auditInto(List<String> findings, String path) {
        if (restriction.isRestricted()) {
            findings.add(String.format("%-34s %-8s %-14s %s",
                    path + "/" + name, sku, restriction.label(),
                    restriction.obligation()));
        }
    }

    /** The RFC 4180 rule, living on a domain class, copy one of two. */
    private static String quote(String field) {
        if (field.indexOf(',') < 0 && field.indexOf('"') < 0) {
            return field;
        }
        return '"' + field.replace("\"", "\"\"") + '"';
    }
}
