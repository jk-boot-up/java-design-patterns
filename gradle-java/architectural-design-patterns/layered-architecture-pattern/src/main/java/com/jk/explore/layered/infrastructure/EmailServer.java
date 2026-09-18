package com.jk.explore.layered.infrastructure;

import java.util.ArrayList;
import java.util.List;

/**
 * Sending the confirmation.
 *
 * <p>Like the card network, it sends nothing and records everything, so a test
 * can assert that exactly one confirmation went out and that it names the order
 * and the total.
 */
public class EmailServer {

    public record Email(String to, String body) {
    }

    private final List<Email> sent = new ArrayList<>();

    public void send(String to, String body) {
        sent.add(new Email(to, body));
    }

    public List<Email> sent() {
        return List.copyOf(sent);
    }
}
