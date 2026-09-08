package com.jk.explore.proxy;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class NaiveAdminImageViewerTest {

    @BeforeEach
    void resetCounter() {
        HighResolutionProductImage.resetLoadCount();
    }

    @Test
    void catalogAdminMayView() {
        NaiveAdminImageViewer viewer = new NaiveAdminImageViewer(new LazyProductImage("SKU-9001"));

        assertEquals("Rendering SKU-9001 hero image (1920x1080)", viewer.view(Role.CATALOG_ADMIN));
    }

    @Test
    void shopperIsDenied() {
        NaiveAdminImageViewer viewer = new NaiveAdminImageViewer(new LazyProductImage("SKU-9001"));

        SecurityException e = assertThrows(SecurityException.class, () -> viewer.view(Role.SHOPPER));
        assertEquals("Only catalog admins may view SKU-9001", e.getMessage());
    }

    @Test
    void duplicatesTheSameCheckAsTheProtectionProxy() {
        NaiveAdminImageViewer naiveViewer = new NaiveAdminImageViewer(new LazyProductImage("SKU-9001"));
        ProductImage proxied = new RestrictedProductImage(new LazyProductImage("SKU-9001"), Role.SHOPPER);

        SecurityException naiveException =
                assertThrows(SecurityException.class, () -> naiveViewer.view(Role.SHOPPER));
        SecurityException proxyException = assertThrows(SecurityException.class, proxied::render);

        assertEquals(naiveException.getMessage(), proxyException.getMessage());
    }
}
