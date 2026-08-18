package com.jk.explore.factorymethod;

/**
 * The product. Every delivery service creates one of these, and every
 * delivery service uses it only through this interface.
 */
public interface Courier {

    String name();

    Shipment dispatch(Order order);
}
