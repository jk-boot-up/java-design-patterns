package com.jk.explore.microkernel;

/** The only thing the core knows about a feature. */
public interface Plugin {

    String name();

    void start();

    void stop();

    /** Takes the running total in cents and returns the new total. */
    long adjust(long cents);
}
