package com.jk.explore.routingslipcamel;

/**
 * An order and the facts that decide which steps it needs.
 */
public record Order(String id, boolean gift, boolean ageRestricted, int customerAge, boolean international, long pence) {
}
