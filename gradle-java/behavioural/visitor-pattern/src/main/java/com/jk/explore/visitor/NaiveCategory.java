package com.jk.explore.visitor;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * The branch, in the naive design.
 *
 * <p>Look at the four report methods: each one is the same loop over the
 * same children, written out again with a different body. That repetition
 * is the traversal, and in the pattern version it exists exactly once, in
 * {@link Category#accept}. Here it exists once per report, so a report that
 * forgets to recurse — or recurses in a different order from its
 * neighbours — is one careless afternoon away.
 */
public final class NaiveCategory implements NaiveCatalogNode {

    private final String name;
    private final List<NaiveCatalogNode> children = new ArrayList<>();

    public NaiveCategory(String name) {
        this.name = name;
    }

    public NaiveCategory add(NaiveCatalogNode child) {
        children.add(child);
        return this;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public Money inventoryValue() {
        Money total = Money.zero();
        for (NaiveCatalogNode child : children) {
            total = total.plus(child.inventoryValue());
        }
        return total;
    }

    @Override
    public void countInto(Map<String, Integer> counts, String path) {
        String here = path.isEmpty() ? name : path + "/" + name;
        counts.putIfAbsent(here, 0);
        for (NaiveCatalogNode child : children) {
            child.countInto(counts, here);
        }
    }

    @Override
    public void appendCsvTo(StringBuilder out, String path) {
        String here = path.isEmpty() ? name : path + "/" + name;
        for (NaiveCatalogNode child : children) {
            child.appendCsvTo(out, here);
        }
    }

    @Override
    public void auditInto(List<String> findings, String path) {
        String here = path.isEmpty() ? name : path + "/" + name;
        for (NaiveCatalogNode child : children) {
            child.auditInto(findings, here);
        }
    }
}
