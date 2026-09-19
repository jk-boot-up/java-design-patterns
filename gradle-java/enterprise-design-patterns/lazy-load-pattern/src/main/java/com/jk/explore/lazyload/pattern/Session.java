package com.jk.explore.lazyload.pattern;

import com.jk.explore.lazyload.toydb.Database;
import com.jk.explore.lazyload.toydb.Row;

/**
 * The connection a lazy load needs. It can be closed, and a load that comes
 * after that fails. That is what happens to a lazy object passed somewhere its
 * session no longer exists.
 */
public class Session {

    private final Database db;
    private boolean open = true;

    public Session(Database db) {
        this.db = db;
    }

    public Row select(String table, int id) {
        if (!open) {
            throw new SessionClosedException("cannot load " + table + " id=" + id + ": the session is closed");
        }
        return db.table(table).select(id);
    }

    public void close() {
        open = false;
    }
}
