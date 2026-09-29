package com.jk.explore.inputvalidation;

import java.util.regex.Pattern;

/**
 * An email address: something, an at sign, a domain with a dot, and not absurdly long.
 */
public record Email(String value) {

    private static final Pattern SHAPE = Pattern.compile("[^@\\s]+@[^@\\s]+\\.[^@\\s]+");

    public Email {
        if (value == null || value.length() > 254 || !SHAPE.matcher(value).matches()) {
            throw new IllegalArgumentException("email address is not valid");
        }
    }
}
