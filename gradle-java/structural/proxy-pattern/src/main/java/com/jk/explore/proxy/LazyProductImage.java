package com.jk.explore.proxy;

/**
 * A virtual proxy. Holds only the SKU until {@link #render()} is actually
 * called, at which point it creates the real subject once and keeps it -- so
 * a listing that never scrolls into view never costs a load, and one that is
 * rendered repeatedly costs exactly one.
 */
public final class LazyProductImage implements ProductImage {

    private final String sku;
    private HighResolutionProductImage realImage;

    public LazyProductImage(String sku) {
        this.sku = sku;
    }

    @Override
    public String render() {
        if (realImage == null) {
            realImage = new HighResolutionProductImage(sku);
        }
        return realImage.render();
    }

    @Override
    public String sku() {
        return sku;
    }
}
