package com.jk.explore.unitofwork.pattern;

import com.jk.explore.unitofwork.toydb.Database;
import com.jk.explore.unitofwork.toydb.Row;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

/**
 * <strong>Register what changed, and write it all at commit.</strong>
 * Nothing touches the database until {@link #commit()}. Commit puts the
 * writes in an order the database will accept, applies them inside one short
 * transaction, and rolls back to exactly what was there if any write fails.
 */
public class UnitOfWork {

    private record Change(String kind, String table, int id, Row row, int rank) {
    }

    private final Database db;
    private final List<String> insertOrder;
    private final List<Change> changes = new ArrayList<>();

    /** @param insertOrder tables in the order inserts must happen, parents first */
    public UnitOfWork(Database db, List<String> insertOrder) {
        this.db = db;
        this.insertOrder = insertOrder;
    }

    public void registerNew(String table, int id, Row row) {
        changes.add(new Change("INSERT", table, id, row, insertOrder.indexOf(table)));
    }

    public void registerDirty(String table, int id, Row row) {
        changes.add(new Change("UPDATE", table, id, row, insertOrder.size()));
    }

    public void registerRemoved(String table, int id) {
        changes.add(new Change("DELETE", table, id, null, insertOrder.size() + 1));
    }

    public int pendingChanges() {
        return changes.size();
    }

    /** Applies every change, parents first, or none of them. */
    public void commit() {
        List<Change> ordered = new ArrayList<>(changes);
        ordered.sort(Comparator.comparingInt(Change::rank));
        db.begin();
        try {
            for (Change c : ordered) {
                switch (c.kind()) {
                    case "INSERT" -> db.table(c.table()).insert(c.id(), c.row());
                    case "UPDATE" -> db.table(c.table()).update(c.id(), c.row());
                    default -> db.table(c.table()).delete(c.id());
                }
            }
            db.commit();
            changes.clear();
        } catch (RuntimeException e) {
            db.rollback();
            changes.clear();
            throw e;
        }
    }

    /** Applies the changes in the order they were registered, with no sorting. For the ordering demo. */
    public void commitInRegistrationOrder() {
        db.begin();
        try {
            for (Change c : changes) {
                switch (c.kind()) {
                    case "INSERT" -> db.table(c.table()).insert(c.id(), c.row());
                    case "UPDATE" -> db.table(c.table()).update(c.id(), c.row());
                    default -> db.table(c.table()).delete(c.id());
                }
            }
            db.commit();
            changes.clear();
        } catch (RuntimeException e) {
            db.rollback();
            changes.clear();
            throw e;
        }
    }
}
