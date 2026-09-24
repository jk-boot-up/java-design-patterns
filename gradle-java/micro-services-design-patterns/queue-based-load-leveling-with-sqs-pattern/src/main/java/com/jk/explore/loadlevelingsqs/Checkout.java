package com.jk.explore.loadlevelingsqs;

import java.util.ArrayList;
import java.util.List;

/** The shop's checkout: it accepts orders and puts them on the queue, and never waits for packing. */
public final class Checkout {

    private Checkout() {
    }

    /** Order ids for a burst of this many orders, numbered on from the first. */
    public static List<String> orders(int first, int count) {
        List<String> ids = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            ids.add("ORD-" + (first + i));
        }
        return ids;
    }
}
