package com.jk.explore.acyclicvisitor;

/**
 * The pattern's root: an empty interface every visitor wears. It names no product type at all.
 *
 * <p>Each product type has its own one-method visitor interface below. A
 * visitor implements only the ones for the products it can handle.
 */
public interface ProductVisitor {

    interface BookVisitor extends ProductVisitor {
        void visit(Products.Book book);
    }

    interface FoodVisitor extends ProductVisitor {
        void visit(Products.Food food);
    }

    interface ElectronicsVisitor extends ProductVisitor {
        void visit(Products.Electronics item);
    }

    /** Added in act three, with the new product type, and nothing else changed. */
    interface GiftCardVisitor extends ProductVisitor {
        void visit(Products.GiftCard card);
    }
}
