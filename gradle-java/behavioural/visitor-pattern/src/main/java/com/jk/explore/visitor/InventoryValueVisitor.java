package com.jk.explore.visitor;

/**
 * Report one: what the stock in the warehouse is worth.
 *
 * <p>The simplest visitor in the project, and the one that shows the shape
 * most clearly: three short methods, one field, and no traversal code at
 * all. It does not extend {@link CategoryPathVisitor} because it genuinely
 * does not care where an item sits — a pound is a pound.
 *
 * <p>The two lines worth reading are the two {@code visit} methods. A
 * product is worth its price times its stock. A bundle is worth its
 * <em>own</em> price times its stock, not the sum of what is in it, because
 * a kit is sold at a discount. One method per node type is what lets those
 * be two plain sentences rather than one sentence with an {@code if} in it.
 */
public final class InventoryValueVisitor implements CatalogVisitor {

    private Money total = Money.zero();
    private int units;
    private int lines;

    @Override
    public void visit(Product product) {
        total = total.plus(product.price().times(product.stockOnHand()));
        units += product.stockOnHand();
        lines++;
    }

    @Override
    public void visit(Bundle bundle) {
        // The kit price, not the contents. Valuing a bundle at the sum of
        // its parts would report stock the shop cannot actually realise.
        total = total.plus(bundle.price().times(bundle.stockOnHand()));
        units += bundle.stockOnHand();
        lines++;
    }

    @Override
    public void visit(Category category) {
        // A category holds no stock of its own. Its children are visited
        // by Category.accept, so there is nothing to do here -- and saying
        // so explicitly is better than an inherited empty method.
    }

    /** What the whole subtree that was walked is worth. */
    public Money total() {
        return total;
    }

    /** How many physical things that is. */
    public int units() {
        return units;
    }

    /** How many sellable lines contributed — products plus bundles. */
    public int lines() {
        return lines;
    }
}
