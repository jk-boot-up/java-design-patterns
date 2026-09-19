package com.jk.explore.delegation;

/** A helper with four methods. A class that wants to look like one, but hands the work on, must write all four. */
public interface Shipping {

    long quoteCents(String destination);

    String carrier();

    int daysToDeliver(String destination);

    boolean canDeliverTo(String destination);
}
