package com.jk.explore.specification.domain;

/** The shop's named rules about products, each written once. */
public final class Products {

    private Products() {
    }

    public static Specification<Product> inStock() {
        return Specification.of("in stock", Product::inStock);
    }

    public static Specification<Product> onSale() {
        return Specification.of("on sale", Product::onSale);
    }

    public static Specification<Product> discontinued() {
        return Specification.of("discontinued", Product::discontinued);
    }

    public static Specification<Product> inCategory(String category) {
        return Specification.of("a " + category, p -> p.category().equals(category));
    }

    /** Strictly under: a product at exactly the limit does not qualify. */
    public static Specification<Product> priceUnder(long pence) {
        return Specification.of("under £" + pence / 100, p -> p.pricePence() < pence);
    }

    /** The rule the search page, the promotion and the shipping offer all mean by "cheap and available". */
    public static Specification<Product> cheapAndAvailable() {
        return inStock().and(priceUnder(1000)).and(discontinued().not());
    }
}
