package com.jk.explore.servant;

/**
 * What the servant needs from anything it ships: a name, a weight and a destination. Nothing more.
 */
public interface Shippable {

    String name();

    int grams();

    String city();
}
