package com.jk.explore.acyclicvisitor;

/**
 * Without the pattern: the classic visitor names every product type, so every visitor must handle every type.
 *
 * <p>Products depend on this interface (to accept it), and it depends on
 * every product: a cycle. A new product type means changing this interface
 * and every class that implements it.
 */
public interface ClassicVisitor {

    void visitBook(Products.Book book);

    void visitFood(Products.Food food);

    void visitElectronics(Products.Electronics item);
}
