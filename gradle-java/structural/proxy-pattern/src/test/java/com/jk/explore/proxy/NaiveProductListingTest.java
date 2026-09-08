package com.jk.explore.proxy;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class NaiveProductListingTest {

    @BeforeEach
    void resetCounter() {
        HighResolutionProductImage.resetLoadCount();
    }

    @Test
    void constructingTheListingEagerlyLoadsEveryImage() {
        new NaiveProductListing(List.of("SKU-1042", "SKU-2087", "SKU-9001"));

        assertEquals(3, HighResolutionProductImage.loadCount());
    }

    @Test
    void renderFirstReturnsTheFirstImage() {
        NaiveProductListing listing = new NaiveProductListing(List.of("SKU-1042", "SKU-2087"));

        assertEquals("Rendering SKU-1042 hero image (1920x1080)", listing.renderFirst());
    }
}
