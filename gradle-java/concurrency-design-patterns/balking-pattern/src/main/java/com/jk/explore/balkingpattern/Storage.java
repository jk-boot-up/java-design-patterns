package com.jk.explore.balkingpattern;

import java.util.ArrayList;
import java.util.List;

/** Where drafts are saved. A write can be held at a gate, to keep a save in progress for as long as the demo likes. */
public class Storage {

    private final List<String> written = new ArrayList<>();
    private volatile Gate holdWrites;
    private volatile Runnable inside = () -> { };

    public synchronized List<String> written() {
        return new ArrayList<>(written);
    }

    public void holdWritesAt(Gate gate, Runnable whenInside) {
        this.holdWrites = gate;
        this.inside = whenInside;
    }

    public void write(String text) {
        inside.run();
        Gate g = holdWrites;
        if (g != null) {
            g.await();
        }
        synchronized (this) {
            written.add(text);
        }
    }
}
