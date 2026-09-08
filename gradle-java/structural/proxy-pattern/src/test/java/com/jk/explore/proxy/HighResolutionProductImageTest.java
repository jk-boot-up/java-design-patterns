package com.jk.explore.proxy;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class HighResolutionProductImageTest {

    @BeforeEach
    void resetCounter() {
        HighResolutionProductImage.resetLoadCount();
    }

    @Test
    void renderReturnsSkuAndResolution() {
        HighResolutionProductImage image = new HighResolutionProductImage("SKU-1042");

        assertEquals("Rendering SKU-1042 hero image (1920x1080)", image.render());
    }

    @Test
    void skuReturnsConstructorArgument() {
        HighResolutionProductImage image = new HighResolutionProductImage("SKU-1042");

        assertEquals("SKU-1042", image.sku());
    }

    @Test
    void constructingIncrementsLoadCount() {
        assertEquals(0, HighResolutionProductImage.loadCount());

        new HighResolutionProductImage("SKU-1042");
        assertEquals(1, HighResolutionProductImage.loadCount());

        new HighResolutionProductImage("SKU-2087");
        assertEquals(2, HighResolutionProductImage.loadCount());
    }
}
