package com.jk.explore.visitor;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Report two: how many sellable lines sit in each category.
 *
 * <p>This is the report that could not have been a method on
 * {@link Product}. A product does not know which category it is in — in
 * this tree, nothing points upwards — so the answer exists only during the
 * walk. {@link CategoryPathVisitor} keeps the path, and this class does
 * nothing but count against it.
 *
 * <p>Two numbers per category, because both are asked for and they are not
 * the same: {@code direct} is what a merchandiser sees on the category
 * page, {@code total} is what a stock report means by "Electronics".
 */
public final class CategoryCountVisitor extends CategoryPathVisitor {

    private final Map<String, Integer> direct = new LinkedHashMap<>();
    private final Map<String, Integer> total = new LinkedHashMap<>();

    @Override
    public void visit(Category category) {
        super.visit(category);
        // Registered on the way in, so an empty category still appears in
        // the report as a zero rather than vanishing from it. A category
        // with nothing in it is exactly the thing the report is for.
        direct.putIfAbsent(path(), 0);
        total.putIfAbsent(path(), 0);
    }

    @Override
    public void visit(Product product) {
        count();
    }

    @Override
    public void visit(Bundle bundle) {
        count();
    }

    /**
     * One line for the category holding it, and one for every category
     * above it — which is the whole difference between the two maps.
     */
    private void count() {
        String here = path();
        direct.merge(here, 1, Integer::sum);
        String walk = "";
        for (String segment : here.split("/")) {
            walk = walk.isEmpty() ? segment : walk + "/" + segment;
            total.merge(walk, 1, Integer::sum);
        }
    }

    /** Lines sitting directly in each category, in tree order. */
    public Map<String, Integer> directCounts() {
        return new LinkedHashMap<>(direct);
    }

    /** Lines anywhere beneath each category, in tree order. */
    public Map<String, Integer> totalCounts() {
        return new LinkedHashMap<>(total);
    }

    /** The categories seen, deepest path last — useful for printing. */
    public int categories() {
        return direct.size();
    }
}
