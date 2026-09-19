package com.jk.explore.proxyspring;

import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Service;

@Service
public class ImageCatalogue {

    private final HighResolutionImage image;
    private final String owner = "catalogue";

    /** {@code @Lazy} here injects a stand-in that builds the real image on its first call. */
    public ImageCatalogue(@Lazy HighResolutionImage image) {
        this.image = image;
    }

    /** A cheap question: answered without touching the image. */
    public String owner() {
        return owner;
    }

    @RequiresRole(Role.CATALOG_ADMIN)
    public String render(String sku) {
        return image.pixels(sku);
    }

    /** Calls its own protected method on this, so the check is skipped. */
    public String renderThroughThis(String sku) {
        return this.render(sku);
    }

    /** A final method cannot be overridden by the generated subclass, so it is not protected. */
    @RequiresRole(Role.CATALOG_ADMIN)
    public final String renderFinal(String sku) {
        return image.pixels(sku);
    }
}
