package com.jk.explore.markerinterface;

/**
 * The shop's products. What kind of care each needs is part of its type.
 */
public final class Products {

    public interface Product {
        String sku();
    }

    public record Milk(String sku) implements Product, Markers.Perishable {
    }

    public record Mug(String sku) implements Product, Markers.Fragile {
    }

    public record Kettle(String sku) implements Product {
    }

    /** A plain class, so that act four can extend it. */
    public static class Yoghurt implements Product, Markers.Perishable {
        private final String sku;

        public Yoghurt(String sku) {
            this.sku = sku;
        }

        public String sku() {
            return sku;
        }
    }

    /** Written later by another team. It is perishable because Yoghurt is: the mark is inherited. */
    public static class YoghurtMultipack extends Yoghurt {
        public YoghurtMultipack(String sku) {
            super(sku);
        }
    }

    private Products() {
    }
}
