package com.jk.explore.executearound;

/** A connection to the order database. It must be closed, and cannot be used after. */
public class Connection {

    private final int id;
    private boolean open = true;

    Connection(int id) {
        this.id = id;
    }

    public String query(String sql) {
        if (!open) {
            throw new IllegalStateException("connection " + id + " is closed");
        }
        return "rows for " + sql;
    }

    void close() {
        open = false;
    }
}
