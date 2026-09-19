package com.jk.explore.datamapper.toydb;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

/** One table: a map from id to a row. Every call is counted by its {@link Database}. */
public final class Table {

    private final String name;
    private final Database database;
    private final Map<Integer, Row> rows = new TreeMap<>();

    Table(String name, Database database) {
        this.name = name;
        this.database = database;
    }

    public void insert(int id, Row row) {
        database.write("INSERT " + name + " id=" + id, () -> rows.put(id, row.copy()));
    }

    public void update(int id, Row row) {
        database.write("UPDATE " + name + " id=" + id, () -> {
            if (!rows.containsKey(id)) {
                throw new IllegalStateException("no row " + id + " in " + name);
            }
            rows.put(id, row.copy());
        });
    }

    public void delete(int id) {
        database.write("DELETE " + name + " id=" + id, () -> rows.remove(id));
    }

    public Row select(int id) {
        database.record("SELECT " + name + " id=" + id);
        Row row = rows.get(id);
        return row == null ? null : row.copy();
    }

    public List<Row> selectWhere(String column, Object value) {
        database.record("SELECT " + name + " WHERE " + column + "=" + value);
        List<Row> found = new ArrayList<>();
        for (Row row : rows.values()) {
            if (value.equals(row.get(column))) {
                found.add(row.copy());
            }
        }
        return found;
    }

    public List<Row> selectAll() {
        database.record("SELECT " + name + " (all)");
        List<Row> all = new ArrayList<>();
        for (Row row : rows.values()) {
            all.add(row.copy());
        }
        return all;
    }

    public int size() {
        return rows.size();
    }

    /** Test and demo back door: the stored row, without counting an operation. */
    public Row peek(int id) {
        Row row = rows.get(id);
        return row == null ? null : row.copy();
    }
}
