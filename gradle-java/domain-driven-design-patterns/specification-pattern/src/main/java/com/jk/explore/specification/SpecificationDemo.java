package com.jk.explore.specification;

import com.jk.explore.specification.domain.Catalogue;
import com.jk.explore.specification.domain.Product;
import com.jk.explore.specification.domain.Products;
import com.jk.explore.specification.domain.Specification;
import com.jk.explore.specification.naive.NaiveShop;

import java.util.ArrayList;
import java.util.List;

public class SpecificationDemo {

    static final Product MUG = new Product("MUG-BLUE", "mug", 800, true, false, false);
    static final Product TENNER = new Product("MUG-RED", "mug", 1000, true, false, false);
    static final Product OLD = new Product("MUG-OLD", "mug", 500, true, false, true);
    static final Product GONE = new Product("MUG-GREEN", "mug", 700, false, false, false);
    static final Product MACHINE = new Product("ESP-001", "machine", 30000, true, true, false);
    static final Product TEA = new Product("TEA-050", "tea", 500, true, true, false);
    static final List<Product> SHELF = List.of(MUG, TENNER, OLD, GONE, MACHINE, TEA);

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    static String skus(List<Product> products) {
        return products.stream().map(Product::sku).toList().toString();
    }

    private static void one() {
        System.out.println("ONE. The same rule, written three times.");
        List<Product> search = SHELF.stream().filter(NaiveShop::showOnSearchPage).toList();
        List<Product> promo = SHELF.stream().filter(NaiveShop::eligibleForPromotion).toList();
        List<Product> shipping = SHELF.stream().filter(NaiveShop::qualifiesForFreeShipping).toList();
        System.out.println("  search page:   " + skus(search));
        System.out.println("  promotion:     " + skus(promo));
        System.out.println("  free shipping: " + skus(shipping));
        System.out.println("  the promotion includes MUG-RED at exactly 10.00 and MUG-OLD, which is discontinued. nobody meant that.");
    }

    private static void two() {
        System.out.println("TWO. The rule, named once.");
        Specification<Product> rule = Products.cheapAndAvailable();
        Catalogue shelf = new Catalogue(SHELF);
        System.out.println("  " + rule.describe());
        System.out.println("  search, promotion and shipping all ask for: " + skus(shelf.select(rule)) + ".");
        System.out.println("  change the rule in one place and all three change.");
    }

    private static void three() {
        System.out.println("THREE. Rules combine.");
        Specification<Product> giftIdea = Products.inCategory("mug").and(Products.priceUnder(1000))
                .or(Products.onSale().and(Products.inCategory("tea")));
        System.out.println("  " + giftIdea.describe());
        System.out.println("  " + skus(new Catalogue(SHELF).select(giftIdea.and(Products.inStock()))) + ", in stock.");
        System.out.println("  three small rules, combined into a fourth, and no new class was written.");
    }

    private static void four() {
        System.out.println("FOUR. A rule can say why not.");
        Specification<Product> rule = Products.cheapAndAvailable();
        for (Product p : List.of(TENNER, OLD, GONE, MUG)) {
            System.out.println("  " + p.sku() + ": " + (rule.isSatisfiedBy(p) ? "qualifies" : "does not qualify, " + rule.unmet(p)));
        }
        System.out.println("  the same object that decides can explain, so an error message is not written by hand.");
    }

    private static void five() {
        System.out.println("FIVE. The same rule, two jobs.");
        Specification<Product> rule = Products.cheapAndAvailable();
        System.out.println("  to select: " + skus(new Catalogue(SHELF).select(rule)) + ".");
        Product chosen = OLD;
        System.out.println("  to validate one product a customer picked, " + chosen.sku() + ": " + (rule.isSatisfiedBy(chosen) ? "ok" : "refused, " + rule.unmet(chosen)) + ".");
        System.out.println("  one definition of cheap and available, used to filter a list and to check a single choice.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        List<Product> big = new ArrayList<>();
        for (int i = 0; i < 10_000; i++) {
            big.add(new Product("SKU-" + i, "mug", 50 + (i % 5000), i % 3 != 0, false, i % 7 == 0));
        }
        Catalogue catalogue = new Catalogue(big);
        List<Product> found = catalogue.select(Products.inStock().and(Products.priceUnder(100)));
        System.out.println("  10000 products. matches: " + found.size() + ". products looked at to find them: " + catalogue.examined() + ".");
        System.out.println("  an in-memory specification looks at everything. to ask the database instead, the rule must be turned into a query.");
        System.out.println("  and for a rule used in one place, a plain lambda in the filter is simpler than a specification.");
    }
}
