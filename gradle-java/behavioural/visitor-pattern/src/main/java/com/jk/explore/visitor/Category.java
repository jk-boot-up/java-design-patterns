package com.jk.explore.visitor;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

/**
 * A branch of the catalog — the Composite, carried over unchanged in shape
 * from {@code structural/composite-pattern}.
 *
 * <p>One thing here is a decision rather than a copy: the walk lives in
 * {@link #accept}, not in the visitors. A visitor is handed the node and
 * then the children, without having to remember to recurse. The Composite
 * project put the recursion in {@code totalPrice()} and {@code print()} for
 * the same reason — a traversal written once cannot be written wrongly the
 * fourth time.
 *
 * <p>It costs something, and {@link CatalogVisitor} says what: a visitor
 * cannot prune. Every report sees the whole tree.
 */
public final class Category implements CatalogComponent {

    private final String name;
    private final List<CatalogComponent> children = new ArrayList<>();

    public Category(String name) {
        this.name = Objects.requireNonNull(name, "name");
    }

    /** Fluent, so a catalog can be written as one expression. */
    public Category add(CatalogComponent child) {
        children.add(Objects.requireNonNull(child, "child"));
        return this;
    }

    @Override
    public String name() {
        return name;
    }

    /** The nodes directly under this one, in the order they were added. */
    public List<CatalogComponent> children() {
        return Collections.unmodifiableList(children);
    }

    /**
     * Depth-first, parents before children, siblings in insertion order —
     * and the same order every time, because a report that changes its row
     * order between runs cannot be diffed.
     *
     * <p>The {@code leave} call at the end is not decoration. A tree walk
     * has two moments at a branch, going in and coming back out, and a
     * report that needs to know which category a product sits in needs both.
     * {@link CategoryCountVisitor} and {@link CsvExportVisitor} use it;
     * {@link InventoryValueVisitor} does not, which is why it is a default
     * method and not an obligation.
     */
    @Override
    public void accept(CatalogVisitor visitor) {
        visitor.visit(this);
        for (CatalogComponent child : children) {
            child.accept(visitor);
        }
        visitor.leave(this);
    }

    @Override
    public String toString() {
        return name + "/ (" + children.size() + " children)";
    }
}
