package com.jk.explore.visitor;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * The bundle, added to the catalog eighteen months after the products —
 * and with it, four more copies of four reports.
 *
 * <p>Two of the four were written by copying {@link NaiveProduct}'s and
 * editing. Both edits are wrong, and neither is stupid:
 *
 * <ul>
 *   <li>{@link #appendCsvTo} dropped the {@code quote} calls. There was no
 *       bundle with a comma in its name on the day it was written, so
 *       nothing failed. Marketing renamed the kit to "Starter Kit, 3 items"
 *       two years later, and finance's spreadsheet gained a column.</li>
 *   <li>{@link #auditInto} checks the bundle's own restriction field, which
 *       is what the product version checked. A bundle has no restriction of
 *       its own; it is restricted by what is in the box. So the kit
 *       containing a lithium cell is reported as clear for air freight.</li>
 * </ul>
 *
 * <p>Neither bug is visible from {@link NaiveCatalogNode}. The interface
 * says the method exists, and both classes have one.
 */
public final class NaiveBundle implements NaiveCatalogNode {

    private final String sku;
    private final String name;
    private final Money price;
    private final int stockOnHand;
    private final List<NaiveProduct> contents = new ArrayList<>();

    /** Copied across with the rest of the class. It is never set. */
    private final Restriction restriction = Restriction.NONE;

    public NaiveBundle(String sku, String name, Money price, int stockOnHand) {
        this.sku = sku;
        this.name = name;
        this.price = price;
        this.stockOnHand = stockOnHand;
    }

    public NaiveBundle containing(NaiveProduct product) {
        contents.add(product);
        return this;
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
        out.append(path).append(',')
                .append(sku).append(',')
                .append(name).append(",bundle,")
                .append(String.format("%.2f", price.asPence() / 100.0)).append(',')
                .append(stockOnHand).append(',')
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
}
