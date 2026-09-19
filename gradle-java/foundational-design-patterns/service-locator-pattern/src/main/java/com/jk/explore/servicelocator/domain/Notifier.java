package com.jk.explore.servicelocator.domain;

/** Tells the customer. The third of the three collaborators. */
public interface Notifier {

    void send(String message);
}
