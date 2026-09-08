package com.jk.explore.visitor;

/**
 * The Element role — a node in the catalog tree.
 *
 * <p>This is the same shape as the Component interface in the Composite
 * project: a {@link Product}, a {@link Bundle} and a whole {@link Category}
 * subtree are all one of these, and client code never asks which. Read
 * {@code structural/composite-pattern} first if that tree is new to you;
 * this project takes it as given and changes only what you do <em>with</em>
 * it.
 *
 * <p>What Visitor adds is the second method. The three questions the
 * Composite project asked of a node — its name, its total price, how many
 * products it holds — were methods here, one per question. That works until
 * the questions keep coming. {@link #accept} is the last method this
 * interface ever needs: it hands the node to a {@link CatalogVisitor}, and
 * every future report is a new visitor rather than a new method.
 *
 * <p>The price of that is stated plainly in {@link CatalogVisitor}: it is
 * paid by the node types, not the operations.
 */
public interface CatalogComponent {

    /** What this node is called — the one thing every report needs. */
    String name();

    /**
     * Hands this node to {@code visitor}, which is the whole pattern.
     *
     * <p>Every implementation is one line, and every implementation is the
     * same line: {@code visitor.visit(this)}. That line is not redundant.
     * It is written inside the class, where {@code this} has a known static
     * type, so the compiler — not an {@code instanceof} chain — picks the
     * overload. See {@link CatalogVisitor} for why that is worth a whole
     * method.
     */
    void accept(CatalogVisitor visitor);
}
