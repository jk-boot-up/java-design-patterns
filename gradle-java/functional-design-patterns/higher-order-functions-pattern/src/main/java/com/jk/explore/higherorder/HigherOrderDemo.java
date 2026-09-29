package com.jk.explore.higherorder;

import static com.jk.explore.higherorder.Catalogue.amountOff;
import static com.jk.explore.higherorder.Catalogue.filter;
import static com.jk.explore.higherorder.Catalogue.inCategory;
import static com.jk.explore.higherorder.Catalogue.inStock;
import static com.jk.explore.higherorder.Catalogue.names;
import static com.jk.explore.higherorder.Catalogue.percentOff;
import static com.jk.explore.higherorder.Catalogue.priceBelow;

import java.util.ArrayList;
import java.util.List;
import java.util.function.DoubleUnaryOperator;
import java.util.function.Predicate;

/**
 * The five acts: a loop per question, passing the test in, making tests to order,
 * price rules as values, and the bill.
 */
public final class HigherOrderDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();
        List<Product> all = Product.catalogue();

        out.add("ONE. A loop for every question.");
        out.add("  under 10: " + names(CopyPasteFilters.under10(all)));
        out.add("  in stock: " + names(CopyPasteFilters.inStock(all)));
        out.add("  mugs:     " + names(CopyPasteFilters.mugs(all)));
        out.add("  3 methods, 3 identical loops; \"mugs under 10 in stock\" would be a 4th");

        out.add("");
        out.add("TWO. One loop; the test is passed in as a function.");
        out.add("  filter(all, p -> p.price() < 10): " + names(filter(all, p -> p.price() < 10)));
        out.add("  filter(all, p -> p.stock() > 0):  " + names(filter(all, p -> p.stock() > 0)));
        out.add("  same answers, one loop");

        out.add("");
        out.add("THREE. Functions that make functions, then combine.");
        Predicate<Product> bargainMugs = priceBelow(10).and(inCategory("mug")).and(inStock());
        out.add("  priceBelow(10).and(inCategory(\"mug\")).and(inStock()): " + names(filter(all, bargainMugs)));
        out.add("  priceBelow(20).and(inStock().negate()):             "
                + names(filter(all, priceBelow(20).and(inStock().negate()))));
        out.add("  new questions are built from small parts, with no new loop");

        out.add("");
        out.add("FOUR. Price rules are values, and can be joined.");
        DoubleUnaryOperator saleThenVoucher = percentOff(20).andThen(amountOff(5));
        DoubleUnaryOperator voucherThenSale = amountOff(5).andThen(percentOff(20));
        out.add("  desk lamp 45.00, 20% off then 5 off: " + String.format("%.2f", saleThenVoucher.applyAsDouble(45)));
        out.add("  desk lamp 45.00, 5 off then 20% off: " + String.format("%.2f", voucherThenSale.applyAsDouble(45)));
        out.add("  the order of the functions matters, and the code shows it");

        out.add("");
        out.add("FIVE. The bill: small functions need good names.");
        out.add("  a chain of anonymous lambdas can hide the rule it implements");
        out.add("  give important ones names, like priceBelow and inStock, and keep each one short");
        out.add("  and an error inside a lambda shows a generated name in the stack trace");
        return out;
    }

    private HigherOrderDemo() {
    }
}
