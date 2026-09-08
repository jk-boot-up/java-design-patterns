package com.jk.explore.composite;

import java.math.BigDecimal;

public final class CatalogDemo {

    public static void main(String[] args) {
        Category electronics = buildCatalog();

        System.out.println("== Printing the whole catalog tree ==");
        electronics.print("");

        System.out.println();
        System.out.println("== Totals, computed uniformly over leaves and composites ==");
        System.out.println("Total price:  $" + electronics.totalPrice());
        System.out.println("Product count: " + electronics.productCount());

        System.out.println();
        System.out.println("== Uniform treatment: no instanceof anywhere above ==");
        for (CatalogComponent child : electronics.children()) {
            System.out.println(child.name() + " -> $" + child.totalPrice()
                    + " across " + child.productCount() + " product(s)");
        }

        System.out.println();
        System.out.println("== The naive alternative, for comparison ==");
        NaiveCategory naiveElectronics = buildNaiveCatalog();
        System.out.println("Total price:  $" + NaiveCatalogPrinter.totalPrice(naiveElectronics));
        System.out.println("Product count: " + NaiveCatalogPrinter.productCount(naiveElectronics));
        System.out.println("Same result, but every one of those three static methods "
                + "repeats the same instanceof chain.");
    }

    private static Category buildCatalog() {
        Category cables = new Category("Cables")
                .add(new Product("USB-C Cable", new BigDecimal("9.99")));

        Category accessories = new Category("Accessories")
                .add(new Product("Case", new BigDecimal("19.99")))
                .add(new Product("Charger", new BigDecimal("29.99")))
                .add(cables);

        return new Category("Electronics")
                .add(new Product("Phone", new BigDecimal("599.99")))
                .add(accessories);
    }

    private static NaiveCategory buildNaiveCatalog() {
        NaiveCategory cables = new NaiveCategory("Cables")
                .add(new NaiveProduct("USB-C Cable", new BigDecimal("9.99")));

        NaiveCategory accessories = new NaiveCategory("Accessories")
                .add(new NaiveProduct("Case", new BigDecimal("19.99")))
                .add(new NaiveProduct("Charger", new BigDecimal("29.99")))
                .add(cables);

        return new NaiveCategory("Electronics")
                .add(new NaiveProduct("Phone", new BigDecimal("599.99")))
                .add(accessories);
    }
}
