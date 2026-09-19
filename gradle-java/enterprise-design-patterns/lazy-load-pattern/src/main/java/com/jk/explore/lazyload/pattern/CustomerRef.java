package com.jk.explore.lazyload.pattern;

/** What a caller sees. It cannot tell whether the customer has been loaded yet. */
public interface CustomerRef {

    String name();
}
