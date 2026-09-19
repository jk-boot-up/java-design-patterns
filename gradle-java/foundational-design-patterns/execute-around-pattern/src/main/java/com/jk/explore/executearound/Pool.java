package com.jk.explore.executearound;

import java.util.function.Function;

/** Hands out connections and counts how many are still out. */
public class Pool {

    private int opened;
    private int stillOpen;

    /** The hand-over version: the caller must call release, on every path. */
    public Connection acquire() {
        opened++;
        stillOpen++;
        return new Connection(opened);
    }

    public void release(Connection c) {
        c.close();
        stillOpen--;
    }

    /** Execute around: open, hand it to the caller's code, and always close. */
    public <T> T withConnection(Function<Connection, T> work) {
        Connection c = acquire();
        try {
            return work.apply(c);
        } finally {
            release(c);
        }
    }

    public int stillOpen() {
        return stillOpen;
    }

    public int opened() {
        return opened;
    }
}
