package com.jk.explore.strategy;

/**
 * The shipping methods, as an enum — the naive design's way of saying which
 * rule applies.
 *
 * <p>Used only by {@link NaiveCheckoutService}. The pattern version has no
 * equivalent: once each rule is an object, an enum naming them adds a second
 * list that has to be kept in step with the first.
 */
public enum ShippingMethod {
    FLAT_RATE,
    WEIGHT_BANDED,
    DISTANCE_BASED,
    FREE_OVER_THRESHOLD
}
