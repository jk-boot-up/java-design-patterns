package com.jk.explore.proxy;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class LazyProductImageTest {

    @BeforeEach
    void resetCounter() {
        HighResolutionProductImage.resetLoadCount();
    }

    @Test
    void skuIsAvailableWithoutLoadingTheRealImage() {
        LazyProductImage proxy = new LazyProductImage("SKU-1042");

        assertEquals("SKU-1042", proxy.sku());
        assertEquals(0, HighResolutionProductImage.loadCount());
    }

    @Test
    void firstRenderLoadsTheRealImage() {
        LazyProductImage proxy = new LazyProductImage("SKU-1042");

        assertEquals("Rendering SKU-1042 hero image (1920x1080)", proxy.render());
        assertEquals(1, HighResolutionProductImage.loadCount());
    }

    @Test
    void secondRenderReusesTheCachedRealImage() {
        LazyProductImage proxy = new LazyProductImage("SKU-1042");

        proxy.render();
        proxy.render();
        proxy.render();

        assertEquals(1, HighResolutionProductImage.loadCount());
    }

    @Test
    void neverRenderingMeansNeverLoading() {
        new LazyProductImage("SKU-1042");
        new LazyProductImage("SKU-2087");

        assertEquals(0, HighResolutionProductImage.loadCount());
    }
}
