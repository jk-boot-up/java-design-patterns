package com.jk.explore.hexagonal.core.port;

/** Telling a customer something happened. Could be email, SMS, or a log line in a test. */
public interface Notifier {

    void send(String to, String body);
}
