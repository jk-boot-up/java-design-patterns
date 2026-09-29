package com.jk.explore.currying;

/**
 * Where a parcel is going, with the carrier's base charge and charge per kilogram.
 */
public enum Zone {
    UK(3.00, 1.00), EU(6.00, 2.00), WORLD(12.00, 4.00);

    final double base;
    final double perKg;

    Zone(double base, double perKg) {
        this.base = base;
        this.perKg = perKg;
    }
}
