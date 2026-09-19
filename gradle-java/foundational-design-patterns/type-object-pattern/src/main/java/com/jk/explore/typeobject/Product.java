package com.jk.explore.typeobject;

/** One class for every product. What differs is in its type. */
public class Product {

    private final String name;
    private final long priceCents;
    private final ProductType type;

    public Product(String name, long priceCents, ProductType type) {
        this.name = name;
        this.priceCents = priceCents;
        this.type = type;
    }

    public String name() {
        return name;
    }

    public ProductType type() {
        return type;
    }

    public long taxCents() {
        return priceCents * type.taxPercent() / 100;
    }

    public long totalCents() {
        return priceCents + taxCents() + type.shippingCents();
    }

    public boolean canReturn(int daysSincePurchase) {
        return daysSincePurchase <= type.returnDays();
    }
}
