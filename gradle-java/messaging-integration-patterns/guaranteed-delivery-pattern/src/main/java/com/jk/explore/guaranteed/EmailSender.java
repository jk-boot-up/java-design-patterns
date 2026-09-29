package com.jk.explore.guaranteed;

import java.util.ArrayList;
import java.util.List;

/**
 * Sends order confirmation emails, and remembers every one it sent (so duplicates can be counted).
 */
public final class EmailSender {

    private final List<String> sent = new ArrayList<>();

    public void send(String id, String body) {
        sent.add(id);
    }

    public List<String> sent() {
        return sent;
    }

    public long duplicates() {
        return sent.size() - sent.stream().distinct().count();
    }
}
