package com.jk.explore.prototype;

/**
 * How a listing ships: carrier, parcel weight, and whether shipping is free.
 *
 * <p>Deliberately a {@code record}. It is immutable, so a {@link
 * ProductListing} copy can share the very same {@code ShippingProfile}
 * instance as the listing it was copied from — nothing can mutate it out
 * from under either one, so there is nothing to deep-copy. Contrast this
 * with {@code images} and {@code attributes} on {@code ProductListing},
 * which are mutable and therefore cannot be shared safely between a
 * prototype and its copies.
 */
public record ShippingProfile(String carrier, int weightGrams, boolean freeShipping) {
}
