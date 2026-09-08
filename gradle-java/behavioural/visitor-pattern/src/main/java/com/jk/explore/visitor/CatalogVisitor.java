package com.jk.explore.visitor;

/**
 * The Visitor role — one report over the catalog tree.
 *
 * <p><strong>What this buys.</strong> Every report in this project is a
 * class that implements this interface, and not one of them required a line
 * of change to {@link Product}, {@link Bundle} or {@link Category}. Total
 * inventory value, a count by category, a CSV export and a compliance audit
 * are four operations over one structure, and the structure has not been
 * edited four times. {@link CatalogReportDemo} writes a fifth report inside
 * the demo file itself to make the point that this is not a claim about
 * these four.
 *
 * <p><strong>What it costs, said as plainly.</strong> The trade runs the
 * other way for node types. Adding a fourth kind of node — a gift card, a
 * digital download — means adding a method here, and <em>every</em>
 * implementation stops compiling until it is written. Four reports today
 * means four classes to edit; the number grows with every report ever
 * written. Visitor is only the right answer when you are confident the set
 * of node types is settled and the set of operations is not. In this
 * catalog that is true — the shape of a shop's catalog changes about once a
 * decade and the reports finance asks for change monthly — and it is
 * genuinely not true everywhere.
 *
 * <p><strong>And the awkward part.</strong> Getting here takes two calls
 * rather than one. {@code node.accept(visitor)} calls
 * {@code visitor.visit(this)} straight back. That round trip is called
 * double dispatch, and it exists because Java picks an overload from the
 * static type of the argument: at a call site holding a
 * {@code CatalogComponent}, {@code visitor.visit(node)} does not compile,
 * because the compiler does not know which of the three methods below is
 * meant. Inside {@code Product.accept}, {@code this} is a {@code Product}
 * and it does. Nobody reads that and finds it obvious the first time, and
 * this project is not going to pretend otherwise — the bounce through
 * {@code accept} is real overhead in reading the code, paid so that no
 * report has to write {@code instanceof}.
 */
public interface CatalogVisitor {

    /** A single item on the shelf. */
    void visit(Product product);

    /**
     * A kit sold as one thing. Separate from {@link #visit(Product)} on
     * purpose: no report treats these the same way, and the compiler is a
     * better place to be reminded of that than a code review is.
     */
    void visit(Bundle bundle);

    /** A branch, on the way in — before any of its children. */
    void visit(Category category);

    /**
     * A branch, on the way back out — after all of its children.
     *
     * <p>A default, because most reports do not care. Making it abstract
     * would put an empty method in half the implementations, and an empty
     * method that must be written is a place for a mistake to hide.
     */
    default void leave(Category category) {
    }
}
