package com.jk.explore.producerconsumer.domain;

/** The slow step: wrapping and labelling one order for the courier. */
@FunctionalInterface
public interface Packing {

    void pack(Order order);
}
