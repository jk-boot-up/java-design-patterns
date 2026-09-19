package com.jk.explore.dependencyinjection.domain;

/** Tells the customer. The third of the three collaborators. */
public interface Notifier {

    void send(String message);
}
