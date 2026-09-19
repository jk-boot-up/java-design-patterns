package com.jk.explore.valueobject.domain;

import java.util.Locale;
import java.util.regex.Pattern;

/**
 * An email address that has already been checked. If you are holding one, it is valid: there is no
 * other way to make one, so no method that receives one ever needs to check again.
 */
public record EmailAddress(String value) {

    private static final Pattern SHAPE = Pattern.compile("^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$");

    public EmailAddress {
        if (value == null || !SHAPE.matcher(value.trim()).matches()) {
            throw new IllegalArgumentException("not an email address: " + value);
        }
        value = value.trim().toLowerCase(Locale.ROOT);
    }

    public static EmailAddress of(String text) {
        return new EmailAddress(text);
    }
}
