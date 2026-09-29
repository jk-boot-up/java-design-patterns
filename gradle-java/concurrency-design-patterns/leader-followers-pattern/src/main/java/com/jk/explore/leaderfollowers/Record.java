package com.jk.explore.leaderfollowers;

import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * What happened to each message: which thread received it, which handled it, and in what order they finished.
 */
public final class Record {

    public record Entry(String id, String receivedBy, String handledBy) {
    }

    private final List<Entry> entries = new CopyOnWriteArrayList<>();
    private final List<String> finished = new CopyOnWriteArrayList<>();

    public void handled(Message m, String receivedBy) {
        pause(m.workMs());
        entries.add(new Entry(m.id(), receivedBy, Thread.currentThread().getName()));
        finished.add(m.id());
    }

    public List<Entry> entries() {
        return entries;
    }

    public List<String> finished() {
        return finished;
    }

    public long sameThread() {
        return entries.stream().filter(e -> e.receivedBy().equals(e.handledBy())).count();
    }

    static void pause(long ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
