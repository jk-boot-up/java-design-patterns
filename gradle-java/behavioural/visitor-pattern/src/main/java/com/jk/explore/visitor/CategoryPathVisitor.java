package com.jk.explore.visitor;

import java.util.ArrayDeque;
import java.util.Deque;

/**
 * A base for the reports that need to know <em>where</em> in the tree they
 * are, rather than only what they are looking at.
 *
 * <p>Three of the four reports need the category path, and the bookkeeping
 * for it is the same every time: push on the way in, pop on the way out.
 * Written three times it would be wrong once. It is the pair of
 * {@code visit(Category)} and {@code leave(Category)} in
 * {@link Category#accept} that makes this possible at all — with only one
 * of the two, a visitor can be told which categories exist but never which
 * one it has finished with.
 *
 * <p>Note what this class is not: it is not part of the pattern, and no
 * node knows it exists. A visitor hierarchy is ordinary code, free to grow
 * a base class the moment two visitors repeat themselves.
 */
public abstract class CategoryPathVisitor implements CatalogVisitor {

    private final Deque<String> path = new ArrayDeque<>();

    @Override
    public void visit(Category category) {
        path.addLast(category.name());
    }

    @Override
    public void leave(Category category) {
        path.removeLast();
    }

    /** Where the walk currently is — {@code "Electronics/Accessories"}. */
    protected String path() {
        return String.join("/", path);
    }

    /** The path a child of the current category would have. */
    protected String pathTo(String childName) {
        return path.isEmpty() ? childName : path() + "/" + childName;
    }

    /** How deep the walk currently is; the root category is depth 1. */
    protected int depth() {
        return path.size();
    }
}
