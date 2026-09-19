package com.jk.explore.dependencyinjection.domain;

import java.util.ArrayList;
import java.util.List;

/** A notifier that remembers what it was asked to send. */
public final class RecordingNotifier implements Notifier {

    private final List<String> sent = new ArrayList<>();

    @Override
    public void send(String message) {
        sent.add(message);
    }

    public List<String> sent() {
        return List.copyOf(sent);
    }
}
