package com.jk.explore.dependencyinjection.container;

/** The container could not build the graph. Raised when it starts, not on the first request. */
public class ContainerFailure extends RuntimeException {

    public ContainerFailure(String message) {
        super(message);
    }
}
