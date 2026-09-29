package com.jk.explore.cas;

/**
 * Something that sells kettles from a limited stock: returns true if a kettle was sold.
 */
public interface Stock {

    boolean buyOne();

    int left();
}
