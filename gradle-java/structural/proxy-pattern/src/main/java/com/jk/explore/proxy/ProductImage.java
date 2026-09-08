package com.jk.explore.proxy;

/**
 * The subject. Both the real image and every proxy standing in for one
 * implement this same interface, so a listing page can never tell which it
 * holds.
 */
public interface ProductImage {

    String render();

    String sku();
}
