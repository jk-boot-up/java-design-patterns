package com.jk.explore.inputvalidation;

import java.util.regex.Pattern;

/**
 * A customer's name: letters from any alphabet, with spaces, apostrophes and hyphens.
 */
public record CustomerName(String value) {

    static final Pattern TOO_STRICT = Pattern.compile("[A-Za-z ]{1,60}");
    static final Pattern FAIR = Pattern.compile("\\p{L}[\\p{L}\\p{M} '\\-]{0,59}");

    public CustomerName {
        if (value == null || !FAIR.matcher(value).matches()) {
            throw new IllegalArgumentException("name may contain letters, spaces, apostrophes and hyphens");
        }
    }
}
