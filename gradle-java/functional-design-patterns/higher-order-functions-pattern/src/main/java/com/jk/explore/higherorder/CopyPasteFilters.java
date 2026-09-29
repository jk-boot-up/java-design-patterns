package com.jk.explore.higherorder;

import java.util.ArrayList;
import java.util.List;

/**
 * Before: one loop per question. The loops are identical except for the test in the middle.
 */
public final class CopyPasteFilters {

    public static List<Product> under10(List<Product> all) {
        List<Product> out = new ArrayList<>();
        for (Product p : all) {
            if (p.price() < 10) {
                out.add(p);
            }
        }
        return out;
    }

    public static List<Product> inStock(List<Product> all) {
        List<Product> out = new ArrayList<>();
        for (Product p : all) {
            if (p.stock() > 0) {
                out.add(p);
            }
        }
        return out;
    }

    public static List<Product> mugs(List<Product> all) {
        List<Product> out = new ArrayList<>();
        for (Product p : all) {
            if (p.category().equals("mug")) {
                out.add(p);
            }
        }
        return out;
    }

    private CopyPasteFilters() {
    }
}
