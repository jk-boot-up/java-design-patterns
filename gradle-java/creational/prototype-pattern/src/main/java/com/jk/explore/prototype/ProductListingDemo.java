package com.jk.explore.prototype;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.NoSuchElementException;

/** Runnable walkthrough of cloning, tweaking, and a prototype registry. */
public final class ProductListingDemo {

    public static void main(String[] args) {
        ShippingProfile standard = new ShippingProfile("ParcelForce", 180, false);

        Map<String, String> baseAttributes = new LinkedHashMap<>();
        baseAttributes.put("color", "Black");
        baseAttributes.put("connectivity", "Bluetooth 5.3");

        ProductListing master = new ProductListing(
                "EARBUD-BLK", "Wireless Earbuds",
                "In-ear wireless earbuds with active noise cancellation.",
                "Electronics", "Acme Audio", Money.pounds(59.99),
                List.of("earbuds-black-1.jpg", "earbuds-black-2.jpg"),
                baseAttributes, standard, 30, 12);

        System.out.println("Master:      " + master);

        // Clone it, then tweak only what makes the white variant different.
        ProductListing whiteVariant = master.copy();
        whiteVariant.setSku("EARBUD-WHT");
        whiteVariant.setTitle("Wireless Earbuds (White)");
        whiteVariant.attributes().put("color", "White");
        whiteVariant.images().clear();
        whiteVariant.images().add("earbuds-white-1.jpg");

        System.out.println("White variant: " + whiteVariant);
        System.out.println("Master after cloning: " + master);
        System.out.println("master.images() unaffected: " + master.images());
        System.out.println("master.attributes() unaffected: " + master.attributes());

        // The immutable ShippingProfile is deliberately shared, not copied.
        System.out.println("shippingProfile is the same instance: "
                + (master.shippingProfile() == whiteVariant.shippingProfile()));

        // A prototype registry: callers ask for a listing by key, never by
        // re-assembling one from scratch.
        ListingRegistry registry = new ListingRegistry();
        registry.register("earbuds-template", master);

        ProductListing firstOrder = registry.create("earbuds-template");
        ProductListing secondOrder = registry.create("earbuds-template");
        firstOrder.setSku("EARBUD-BLU");
        firstOrder.attributes().put("color", "Blue");

        System.out.println("first from registry:  " + firstOrder);
        System.out.println("second from registry: " + secondOrder);
        System.out.println("registry copies are independent instances: "
                + (firstOrder != secondOrder));

        try {
            registry.create("does-not-exist");
        } catch (NoSuchElementException e) {
            System.out.println("Rejected: " + e.getMessage());
        }
    }
}
