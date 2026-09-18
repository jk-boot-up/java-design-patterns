package com.jk.explore.hexagonal.adapter.notification;

import com.jk.explore.hexagonal.core.port.Notifier;

import java.util.ArrayList;
import java.util.List;

/** Sends nothing, records everything — a stand-in for email, SMS, or whatever a real adapter chooses. */
public class InMemoryNotifier implements Notifier {

    public record Sent(String to, String body) {
    }

    private final List<Sent> sent = new ArrayList<>();

    @Override
    public void send(String to, String body) {
        sent.add(new Sent(to, body));
    }

    public List<Sent> sent() {
        return List.copyOf(sent);
    }
}
