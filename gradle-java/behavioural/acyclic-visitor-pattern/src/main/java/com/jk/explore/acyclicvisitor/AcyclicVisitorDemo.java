package com.jk.explore.acyclicvisitor;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: the classic visitor, the acyclic visitor, a new product type, a visitor for one type, and the bill.
 */
public final class AcyclicVisitorDemo {

    static final List<Products.Product> BASKET = List.of(
            new Products.Book("BOOK-1", 2000),
            new Products.Food("TEA-1", 400),
            new Products.Electronics("KETTLE-1", 3000, 1200));

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. The classic visitor names every product type.");
        Visitors.ClassicVat classic = new Visitors.ClassicVat();
        BASKET.forEach(p -> p.acceptClassic(classic));
        out.add("  VAT on a book, tea and a kettle: " + pounds(classic.vatPence()));
        out.add("  ClassicVisitor has " + ClassicVisitor.class.getDeclaredMethods().length
                + " methods, one per product type; every visitor must write all of them");
        out.add("  the customs visitor has 2 empty methods, only to satisfy the interface");
        try {
            new Products.GiftCard("GIFT-1", 5000).acceptClassic(classic);
        } catch (UnsupportedOperationException e) {
            out.add("  a gift card arrives: " + e.getMessage());
        }

        out.add("");
        out.add("TWO. The acyclic visitor: one small interface per product type.");
        Visitors.Vat vat = new Visitors.Vat();
        BASKET.forEach(p -> p.accept(vat));
        out.add("  the VAT visitor implements Book, Food and Electronics visitors: " + pounds(vat.vatPence()));
        out.add("  ProductVisitor itself names no product type, so there is no cycle");

        out.add("");
        out.add("THREE. A new product type, and nothing old changes.");
        List<Products.Product> withGift = new ArrayList<>(BASKET);
        withGift.add(new Products.GiftCard("GIFT-1", 5000));
        Visitors.GiftCardActivation activation = new Visitors.GiftCardActivation();
        Visitors.Vat vat2 = new Visitors.Vat();
        for (Products.Product p : withGift) {
            p.accept(activation);
            if (!p.accept(vat2)) {
                out.add("  VAT visitor skips " + p.sku() + ": it does not handle gift cards");
            }
        }
        out.add("  the new activation visitor handled: " + activation.activated());
        out.add("  VAT is still " + pounds(vat2.vatPence()) + "; the VAT and customs classes were not touched");

        out.add("");
        out.add("FOUR. A visitor for exactly the types it cares about.");
        Visitors.Customs customs = new Visitors.Customs();
        long handled = withGift.stream().filter(p -> p.accept(customs)).count();
        out.add("  customs visitor implements only ElectronicsVisitor: handled " + handled + " of " + withGift.size());
        out.add("  " + customs.forms());

        out.add("");
        out.add("FIVE. The bill: mistakes show up only when the code runs.");
        ProductVisitor forgetful = (ProductVisitor.BookVisitor) book -> { };
        out.add("  a VAT visitor that forgot FoodVisitor still compiles");
        out.add("  at run time, tea accepted: " + BASKET.get(1).accept(forgetful) + ", and nobody was told");
        out.add("  and there is one extra interface for every product type");
        return out;
    }

    static String pounds(long pence) {
        return String.format("£%d.%02d", pence / 100, pence % 100);
    }

    private AcyclicVisitorDemo() {
    }
}
