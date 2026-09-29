package com.jk.explore.lenses;

/**
 * A delivery address. Records are immutable: a change means a new Address.
 */
public record Address(String street, String city, String postcode) {
}
