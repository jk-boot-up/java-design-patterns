package com.jk.explore.eda;

import java.util.ArrayList;
import java.util.List;

/** An append-only log. Events are never changed or removed, so anyone can read from any point. */
public class EventLog {

    private final List<Event> events = new ArrayList<>();

    public int append(String type, String orderId) {
        int offset = events.size();
        events.add(new Event(offset, type, orderId));
        return offset;
    }

    public List<Event> readFrom(int offset) {
        return List.copyOf(events.subList(Math.min(offset, events.size()), events.size()));
    }

    public int size() {
        return events.size();
    }
}
