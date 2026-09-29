package com.jk.explore.inputvalidation;

/**
 * What arrives from the browser: every field is just text, and none of it can be trusted.
 */
public record OrderForm(String sku, String quantity, String email, String name) {
}
