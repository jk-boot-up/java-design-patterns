package com.jk.explore.composite;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CategoryTest {

    @Test
    void emptyCategoryHasZeroPriceAndZeroProducts() {
        Category empty = new Category("Empty");

        assertEquals(BigDecimal.ZERO, empty.totalPrice());
        assertEquals(0, empty.productCount());
    }

    @Test
    void totalPriceSumsDirectProductChildren() {
        Category accessories = new Category("Accessories")
                .add(new Product("Case", new BigDecimal("19.99")))
                .add(new Product("Charger", new BigDecimal("29.99")));

        assertEquals(new BigDecimal("49.98"), accessories.totalPrice());
    }

    @Test
    void totalPriceRecursesThroughNestedCategories() {
        Category cables = new Category("Cables")
                .add(new Product("USB-C Cable", new BigDecimal("9.99")));
        Category accessories = new Category("Accessories")
                .add(new Product("Case", new BigDecimal("19.99")))
                .add(cables);
        Category electronics = new Category("Electronics")
                .add(new Product("Phone", new BigDecimal("599.99")))
                .add(accessories);

        assertEquals(new BigDecimal("629.97"), electronics.totalPrice());
    }

    @Test
    void productCountRecursesThroughNestedCategories() {
        Category cables = new Category("Cables")
                .add(new Product("USB-C Cable", new BigDecimal("9.99")));
        Category accessories = new Category("Accessories")
                .add(new Product("Case", new BigDecimal("19.99")))
                .add(new Product("Charger", new BigDecimal("29.99")))
                .add(cables);
        Category electronics = new Category("Electronics")
                .add(new Product("Phone", new BigDecimal("599.99")))
                .add(accessories);

        assertEquals(4, electronics.productCount());
    }

    @Test
    void childrenIsUnmodifiable() {
        Category category = new Category("Electronics")
                .add(new Product("Phone", new BigDecimal("599.99")));

        assertTrue(category.children().size() == 1);
        org.junit.jupiter.api.Assertions.assertThrows(UnsupportedOperationException.class,
                () -> category.children().add(new Product("Tablet", BigDecimal.TEN)));
    }

    @Test
    void aCategoryTreatsProductAndCategoryChildrenUniformly() {
        Category cables = new Category("Cables")
                .add(new Product("USB-C Cable", new BigDecimal("9.99")));
        Category mixed = new Category("Mixed")
                .add(new Product("Phone", new BigDecimal("599.99")))
                .add(cables);

        for (CatalogComponent child : mixed.children()) {
            assertTrue(child.totalPrice().compareTo(BigDecimal.ZERO) > 0);
        }
    }
}
