package com.jk.explore.acyclicvisitor;

import java.util.ArrayList;
import java.util.List;

/**
 * The shop's visitors. Each picks the product types it handles by which small interfaces it implements.
 */
public final class Visitors {

    /** VAT at 20% on electronics; books and food are zero-rated. Handles those three types only. */
    public static final class Vat implements ProductVisitor.BookVisitor, ProductVisitor.FoodVisitor,
            ProductVisitor.ElectronicsVisitor {

        private long vatPence;

        public void visit(Products.Book book) {
        }

        public void visit(Products.Food food) {
        }

        public void visit(Products.Electronics item) {
            vatPence += item.pricePence() * 20 / 100;
        }

        public long vatPence() {
            return vatPence;
        }
    }

    /** Customs forms are only needed for electronics, so this visitor handles electronics and nothing else. */
    public static final class Customs implements ProductVisitor.ElectronicsVisitor {

        private final List<String> forms = new ArrayList<>();

        public void visit(Products.Electronics item) {
            forms.add("form for " + item.sku() + ", " + item.grams() + " g");
        }

        public List<String> forms() {
            return forms;
        }
    }

    /** Written with the gift card type, in act three. Existing visitors did not change. */
    public static final class GiftCardActivation implements ProductVisitor.GiftCardVisitor {

        private final List<String> activated = new ArrayList<>();

        public void visit(Products.GiftCard card) {
            activated.add(card.sku());
        }

        public List<String> activated() {
            return activated;
        }
    }

    /** The classic VAT visitor: forced to have a method for every type, whether it cares or not. */
    public static final class ClassicVat implements ClassicVisitor {

        private long vatPence;

        public void visitBook(Products.Book book) {
        }

        public void visitFood(Products.Food food) {
        }

        public void visitElectronics(Products.Electronics item) {
            vatPence += item.pricePence() * 20 / 100;
        }

        public long vatPence() {
            return vatPence;
        }
    }

    /** The classic customs visitor: two of its three methods are empty, only to satisfy the interface. */
    public static final class ClassicCustoms implements ClassicVisitor {

        public void visitBook(Products.Book book) {
        }

        public void visitFood(Products.Food food) {
        }

        public void visitElectronics(Products.Electronics item) {
        }
    }

    private Visitors() {
    }
}
