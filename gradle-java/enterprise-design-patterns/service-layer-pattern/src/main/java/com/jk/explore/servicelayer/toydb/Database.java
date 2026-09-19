package com.jk.explore.servicelayer.toydb;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * <strong>The toy database every project in this category copies.</strong>
 * Five properties and no more: rows rather than objects; a visible operation
 * counter; an explicit {@link #flush()} when buffering is switched on;
 * failure on demand; and no threading at all.
 */
public final class Database {

    private final Map<String, Table> tables = new HashMap<>();
    private final List<String> log = new ArrayList<>();
    private final List<Runnable> staged = new ArrayList<>();
    private boolean buffered;
    private int failAfterWrites = -1;

    private final Map<String, String[]> parents = new HashMap<>();
    private Map<String, Map<Integer, Row>> savepoint;

    /** A row in {@code child} must name an existing row of {@code parent} in {@code column}. */
    public void requireParent(String child, String column, String parent) {
        parents.put(child, new String[]{column, parent});
    }

    void checkParent(String child, Row row) {
        String[] rule = parents.get(child);
        if (rule != null && table(rule[1]).peek(row.number(rule[0])) == null) {
            throw new IllegalStateException("foreign key: " + child + "." + rule[0] + "=" + row.number(rule[0])
                    + " has no row in " + rule[1]);
        }
    }

    /** Starts a transaction: remembers every table as it is now. */
    public void begin() {
        savepoint = new HashMap<>();
        tables.forEach((n, t) -> savepoint.put(n, t.snapshot()));
    }

    public void commit() {
        savepoint = null;
    }

    /** Puts every table back as it was at {@link #begin()}. */
    public void rollback() {
        if (savepoint != null) {
            savepoint.forEach((n, snap) -> table(n).restore(snap));
            tables.forEach((n, t) -> {
                if (!savepoint.containsKey(n)) {
                    t.restore(new java.util.TreeMap<>());
                }
            });
            savepoint = null;
        }
    }

    public Table table(String name) {
        return tables.computeIfAbsent(name, n -> new Table(n, this));
    }

    /** Every operation issued so far, in order, as the SQL-shaped line it stands for. */
    public List<String> operations() {
        return List.copyOf(log);
    }

    public int operationCount() {
        return log.size();
    }

    public void clearLog() {
        log.clear();
    }

    /** From now on, writes wait in a buffer until {@link #flush()}. */
    public void buffered(boolean on) {
        this.buffered = on;
    }

    /** Applies every staged write, in order. */
    public void flush() {
        List<Runnable> toApply = new ArrayList<>(staged);
        staged.clear();
        toApply.forEach(Runnable::run);
    }

    public int stagedWrites() {
        return staged.size();
    }

    /** The write after the next {@code writesBeforeFailure} writes will be rejected. */
    public void failWriteNumber(int writesFromNow) {
        this.failAfterWrites = writesFromNow - 1;
    }

    void record(String operation) {
        log.add(operation);
    }

    void write(String operation, Runnable apply) {
        Runnable checked = () -> {
            if (failAfterWrites == 0) {
                failAfterWrites = -1;
                log.add(operation + "  -> REJECTED");
                throw new IllegalStateException("the database rejected: " + operation);
            }
            if (failAfterWrites > 0) {
                failAfterWrites--;
            }
            log.add(operation);
            apply.run();
        };
        if (buffered) {
            staged.add(checked);
        } else {
            checked.run();
        }
    }
}
