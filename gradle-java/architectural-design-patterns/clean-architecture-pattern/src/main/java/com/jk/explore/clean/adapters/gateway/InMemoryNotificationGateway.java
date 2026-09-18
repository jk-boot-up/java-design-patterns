package com.jk.explore.clean.adapters.gateway;

import com.jk.explore.clean.usecases.NotificationGateway;

import java.util.ArrayList;
import java.util.List;

public class InMemoryNotificationGateway implements NotificationGateway {

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
