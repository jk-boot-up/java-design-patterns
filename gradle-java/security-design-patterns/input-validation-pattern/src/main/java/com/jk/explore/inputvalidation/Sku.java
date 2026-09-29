package com.jk.explore.inputvalidation;

import java.util.regex.Pattern;

/**
 * A product code. If one of these exists, it is valid: the check happens once, here.
 */
public record Sku(String value) {

    private static final Pattern SHAPE = Pattern.compile("[A-Z]{3}-\\d{1,6}");

    public Sku {
        if (value == null || !SHAPE.matcher(value).matches()) {
            throw new IllegalArgumentException("product code must look like MUG-12");
        }
    }
}
