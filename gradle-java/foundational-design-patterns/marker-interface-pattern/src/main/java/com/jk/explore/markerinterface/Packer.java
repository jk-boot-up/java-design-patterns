package com.jk.explore.markerinterface;

import java.util.ArrayList;
import java.util.List;

/**
 * The warehouse packer and the chilled courier, both deciding by type.
 */
public final class Packer {

    public static String pack(Products.Product p) {
        List<String> extras = new ArrayList<>();
        if (p instanceof Markers.Perishable) {
            extras.add("ice packs");
        }
        if (p instanceof Markers.Fragile) {
            extras.add("bubble wrap");
        }
        return p.sku() + ": " + (extras.isEmpty() ? "plain box" : String.join(" + ", extras));
    }

    /** Only perishable things can even be handed to this courier: the compiler checks the parameter type. */
    public static String sendChilled(Markers.Perishable item) {
        return "chilled van takes " + ((Products.Product) item).sku();
    }

    private Packer() {
    }
}
