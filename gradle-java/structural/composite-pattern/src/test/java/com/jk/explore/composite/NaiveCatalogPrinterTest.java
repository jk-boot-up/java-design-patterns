package com.jk.explore.composite;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class NaiveCatalogPrinterTest {

    @Test
    void totalPriceMatchesTheCompositeEquivalent() {
        NaiveCategory cables = new NaiveCategory("Cables")
                .add(new NaiveProduct("USB-C Cable", new BigDecimal("9.99")));
        NaiveCategory accessories = new NaiveCategory("Accessories")
                .add(new NaiveProduct("Case", new BigDecimal("19.99")))
                .add(cables);
        NaiveCategory electronics = new NaiveCategory("Electronics")
                .add(new NaiveProduct("Phone", new BigDecimal("599.99")))
                .add(accessories);

        assertEquals(new BigDecimal("629.97"), NaiveCatalogPrinter.totalPrice(electronics));
    }

    @Test
    void productCountMatchesTheCompositeEquivalent() {
        NaiveCategory accessories = new NaiveCategory("Accessories")
                .add(new NaiveProduct("Case", new BigDecimal("19.99")))
                .add(new NaiveProduct("Charger", new BigDecimal("29.99")));
        NaiveCategory electronics = new NaiveCategory("Electronics")
                .add(new NaiveProduct("Phone", new BigDecimal("599.99")))
                .add(accessories);

        assertEquals(3, NaiveCatalogPrinter.productCount(electronics));
    }

    @Test
    void unknownItemTypeThrows() {
        assertThrows(IllegalArgumentException.class,
                () -> NaiveCatalogPrinter.totalPrice("not a catalog item"));
    }
}
