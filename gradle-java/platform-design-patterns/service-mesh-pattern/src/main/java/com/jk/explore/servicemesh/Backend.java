package com.jk.explore.servicemesh;

/** A service that can be called. It answers yes or no. */
public interface Backend {

    boolean call();

    int received();
}
