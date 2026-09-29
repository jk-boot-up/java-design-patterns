package com.jk.explore.extensionobject;

import java.util.ArrayList;
import java.util.List;

/**
 * After payment, asks each product which extra roles it has, and acts on the ones it recognises.
 */
public final class Checkout {

    public static List<String> afterPayment(List<Product> basket) {
        List<String> actions = new ArrayList<>();
        for (Product p : basket) {
            p.extension(Extensions.Download.class).ifPresent(d ->
                    actions.add(p.sku() + ": email link " + d.url() + " (" + d.maxDownloads() + " downloads)"));
            p.extension(Extensions.Warranty.class).ifPresent(w ->
                    actions.add(p.sku() + ": register a " + w.years() + "-year warranty"));
            p.extension(Extensions.Subscription.class).ifPresent(s ->
                    actions.add(p.sku() + ": schedule a delivery every " + s.everyWeeks() + " weeks"));
        }
        return actions;
    }

    private Checkout() {
    }
}
