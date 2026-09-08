package com.jk.explore.proxy;

import java.util.List;

public final class ProductImageDemo {

    private ProductImageDemo() {
    }

    public static void main(String[] args) {
        HighResolutionProductImage.resetLoadCount();

        System.out.println("== Naive listing -- eagerly loads every image, even ones never scrolled to ==");
        NaiveProductListing naiveListing =
                new NaiveProductListing(List.of("SKU-1042", "SKU-2087", "SKU-9001"));
        System.out.println("Images loaded eagerly, before rendering anything: "
                + HighResolutionProductImage.loadCount());
        System.out.println("Naive listing render: " + naiveListing.renderFirst());

        HighResolutionProductImage.resetLoadCount();

        System.out.println();
        System.out.println("== Virtual proxy -- loads an image only when it's actually rendered ==");
        ProductImage lazy = new LazyProductImage("SKU-1042");
        System.out.println("Images loaded so far (real subject not yet touched): "
                + HighResolutionProductImage.loadCount());
        System.out.println("Proxy render: " + lazy.render());
        System.out.println("Images loaded after first render: " + HighResolutionProductImage.loadCount());
        System.out.println("Proxy render (again): " + lazy.render());
        System.out.println("Images loaded after second render (unchanged -- cached): "
                + HighResolutionProductImage.loadCount());

        System.out.println();
        System.out.println("== Protection proxy -- controls access to render() based on role ==");
        ProductImage guarded = new RestrictedProductImage(new LazyProductImage("SKU-2087"), Role.CATALOG_ADMIN);
        System.out.println("Catalog admin can render: " + guarded.render());
        ProductImage denied = new RestrictedProductImage(new LazyProductImage("SKU-2087"), Role.SHOPPER);
        try {
            denied.render();
        } catch (SecurityException e) {
            System.out.println("Shopper denied: " + e.getMessage());
        }

        System.out.println();
        System.out.println("== Composing proxies -- protection proxy wrapping a virtual proxy ==");
        System.out.println("Total images loaded so far: " + HighResolutionProductImage.loadCount()
                + " -- SKU-9001 is not among them yet, still lazy");
        ProductImage composed = new RestrictedProductImage(new LazyProductImage("SKU-9001"), Role.CATALOG_ADMIN);
        System.out.println("Admin render through both proxies: " + composed.render());
        System.out.println("Total images loaded after admin render: " + HighResolutionProductImage.loadCount());

        System.out.println();
        System.out.println("== The naive alternative for access control, for comparison ==");
        NaiveAdminImageViewer naiveViewer = new NaiveAdminImageViewer(new LazyProductImage("SKU-9001"));
        try {
            naiveViewer.view(Role.SHOPPER);
        } catch (SecurityException e) {
            System.out.println("Naive viewer denied: " + e.getMessage());
        }
        System.out.println("Same check, duplicated in every screen that needs it -- "
                + "a protection proxy centralises it once, for any ProductImage.");
    }
}
