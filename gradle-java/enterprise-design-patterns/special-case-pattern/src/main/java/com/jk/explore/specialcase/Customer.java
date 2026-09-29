package com.jk.explore.specialcase;

/**
 * Everything checkout needs from a customer. Registered customers, guests and unknown customers all answer it.
 */
public interface Customer {

    String name();

    long points();

    void earnPoints(long spentPence);

    int discountPercent();

    boolean canReceiveMarketing();
}
