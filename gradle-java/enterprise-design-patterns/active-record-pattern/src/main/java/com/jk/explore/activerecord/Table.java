package com.jk.explore.activerecord;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

/** A very small table of rows, each a map of column to value. Every read and write is counted. */
public class Table {

    private final Map<Integer, Map<String, Object>> rows = new HashMap<>();
    private final AtomicInteger nextId = new AtomicInteger(1);
    private final AtomicInteger operations = new AtomicInteger();

    public int operations() {
        return operations.get();
    }

    public void resetCount() {
        operations.set(0);
    }

    public int insert(Map<String, Object> row) {
        operations.incrementAndGet();
        int id = nextId.getAndIncrement();
        rows.put(id, new HashMap<>(row));
        return id;
    }

    public void update(int id, Map<String, Object> row) {
        operations.incrementAndGet();
        rows.put(id, new HashMap<>(row));
    }

    public Map<String, Object> find(int id) {
        operations.incrementAndGet();
        Map<String, Object> row = rows.get(id);
        return row == null ? null : new HashMap<>(row);
    }

    public List<Integer> whereEquals(String column, Object value) {
        operations.incrementAndGet();
        List<Integer> ids = new ArrayList<>();
        rows.forEach((id, row) -> {
            if (value.equals(row.get(column))) {
                ids.add(id);
            }
        });
        ids.sort(Integer::compare);
        return ids;
    }

    /** The schema changes under the code: a column gets a new name. */
    public void renameColumn(String from, String to) {
        rows.values().forEach(row -> row.put(to, row.remove(from)));
    }
}
