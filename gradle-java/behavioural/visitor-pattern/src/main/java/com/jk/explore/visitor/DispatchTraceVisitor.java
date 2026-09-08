package com.jk.explore.visitor;

import java.util.ArrayList;
import java.util.List;

/**
 * Not a report — a way of seeing the mechanism.
 *
 * <p>It records which of the three {@code visit} overloads ran for each
 * node, and in what order. Printed next to the tree it shows the two things
 * that are hard to believe from reading the code: that every node reached
 * the method matching its own type without a single {@code instanceof}, and
 * that the walk order came from {@link Category#accept} rather than from
 * any visitor.
 *
 * <p>It is also the cheapest possible demonstration of the pattern's whole
 * claim. This class is a report the catalog was never designed for, written
 * long after {@link Product} and {@link Category} were finished, and it
 * needed no change to either.
 */
public final class DispatchTraceVisitor extends CategoryPathVisitor {

    private final List<String> trace = new ArrayList<>();
    private int products;
    private int bundles;
    private int categories;

    @Override
    public void visit(Category category) {
        super.visit(category);
        categories++;
        record("visit(Category)", category.name() + "/");
    }

    @Override
    public void leave(Category category) {
        record("leave(Category)", category.name() + "/");
        super.leave(category);
    }

    @Override
    public void visit(Product product) {
        products++;
        record("visit(Product)", product.name());
    }

    @Override
    public void visit(Bundle bundle) {
        bundles++;
        record("visit(Bundle)", bundle.name());
    }

    private void record(String method, String node) {
        // Indented by depth, so the printed trace has the shape of the tree
        // it walked. leave() is recorded after the pop for categories, so
        // the two lines for one category line up.
        String indent = "  ".repeat(Math.max(0, depth() - 1));
        trace.add(String.format("%-16s %s%s", method, indent, node));
    }

    /** The walk, one line per call, in the order the calls happened. */
    public List<String> trace() {
        return List.copyOf(trace);
    }

    public int products() {
        return products;
    }

    public int bundles() {
        return bundles;
    }

    public int categories() {
        return categories;
    }
}
