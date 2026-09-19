package com.jk.explore.lazyload.pattern;

/** The hand-built cousin of Hibernate's LazyInitializationException. */
public class SessionClosedException extends RuntimeException {

    public SessionClosedException(String message) {
        super(message);
    }
}
