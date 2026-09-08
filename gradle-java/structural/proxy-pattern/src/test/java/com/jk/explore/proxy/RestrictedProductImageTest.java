package com.jk.explore.proxy;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class RestrictedProductImageTest {

    @BeforeEach
    void resetCounter() {
        HighResolutionProductImage.resetLoadCount();
    }

    @Test
    void catalogAdminMayRender() {
        ProductImage image =
                new RestrictedProductImage(new HighResolutionProductImage("SKU-2087"), Role.CATALOG_ADMIN);

        assertEquals("Rendering SKU-2087 hero image (1920x1080)", image.render());
    }

    @Test
    void shopperIsDeniedWithoutTouchingTheWrappedImage() {
        ProductImage image = new RestrictedProductImage(new LazyProductImage("SKU-2087"), Role.SHOPPER);

        SecurityException e = assertThrows(SecurityException.class, image::render);
        assertEquals("Only catalog admins may view SKU-2087", e.getMessage());
        assertEquals(0, HighResolutionProductImage.loadCount());
    }

    @Test
    void skuIsAvailableRegardlessOfRole() {
        ProductImage image = new RestrictedProductImage(new LazyProductImage("SKU-2087"), Role.SHOPPER);

        assertEquals("SKU-2087", image.sku());
    }

    @Test
    void composesWithAVirtualProxyForLazyAndProtectedAccess() {
        ProductImage composed =
                new RestrictedProductImage(new LazyProductImage("SKU-9001"), Role.CATALOG_ADMIN);

        assertEquals(0, HighResolutionProductImage.loadCount());
        assertEquals("Rendering SKU-9001 hero image (1920x1080)", composed.render());
        assertEquals(1, HighResolutionProductImage.loadCount());
    }
}
