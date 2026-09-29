package com.jk.explore.singletable;

/**
 * The shop's product types. They share a code, a name and a price; each adds one field of its own.
 */
public final class Products {

    public sealed interface Product permits Book, Food, Electronics, GiftCard {
        String sku();

        String name();

        int pricePence();

        /** What the packing slip says about this kind of product. */
        String packingNote();
    }

    public record Book(String sku, String name, int pricePence, String isbn) implements Product {
        public String packingNote() {
            return "ISBN " + isbn;
        }
    }

    public record Food(String sku, String name, int pricePence, String bestBefore) implements Product {
        public String packingNote() {
            return "best before " + bestBefore;
        }
    }

    public record Electronics(String sku, String name, int pricePence, Integer warrantyYears) implements Product {
        public String packingNote() {
            return warrantyYears + "-year warranty card";
        }
    }

    /** Added in act four: one new class and one new column. */
    public record GiftCard(String sku, String name, int pricePence, Integer valuePence) implements Product {
        public String packingNote() {
            return "activate £" + valuePence / 100 + " on dispatch";
        }
    }

    private Products() {
    }
}
