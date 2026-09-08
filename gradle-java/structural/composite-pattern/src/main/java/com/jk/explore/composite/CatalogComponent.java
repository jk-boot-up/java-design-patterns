package com.jk.explore.composite;

import java.math.BigDecimal;

/**
 * The Component role. Both a single {@link Product} and a whole
 * {@link Category} subtree answer these same three questions the same way,
 * so client code never needs to ask "is this a leaf or a branch?" first.
 */
public interface CatalogComponent {

    String name();

    BigDecimal totalPrice();

    int productCount();

    void print(String indent);
}
