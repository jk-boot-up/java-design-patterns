package com.jk.explore.eda;

import java.util.HashSet;
import java.util.Set;
import java.util.function.Consumer;

/** One service reading the log at its own pace. It remembers how far it has read. */
public class Reactor {

    private final String name;
    private final Consumer<Event> reaction;
    private final boolean idempotent;
    private final Set<Integer> seen = new HashSet<>();
    private int next = 0;
    private boolean up = true;

    public Reactor(String name, boolean idempotent, Consumer<Event> reaction) {
        this.name = name;
        this.idempotent = idempotent;
        this.reaction = reaction;
    }

    public String name() {
        return name;
    }

    public void goDown() {
        up = false;
    }

    public void comeUp() {
        up = true;
    }

    /** Reads everything new, if it is up. Returns how many events it reacted to. */
    public int poll(EventLog log) {
        if (!up) {
            return 0;
        }
        int reacted = 0;
        for (Event e : log.readFrom(next)) {
            next = e.offset() + 1;
            if (idempotent && !seen.add(e.offset())) {
                continue;
            }
            reaction.accept(e);
            reacted++;
        }
        return reacted;
    }

    /** Delivers the same event again, as a broker may after a missed acknowledgement. */
    public void redeliver(Event e) {
        if (idempotent && !seen.add(e.offset())) {
            return;
        }
        reaction.accept(e);
    }

    public int lag(EventLog log) {
        return log.size() - next;
    }

    public void rewind() {
        next = 0;
        seen.clear();
    }
}
