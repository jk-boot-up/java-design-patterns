package com.jk.explore.identitymap.toydb;

import java.util.LinkedHashMap;
import java.util.Map;

/** A row: column names to values. Not an object, on purpose. */
public final class Row {

    private final Map<String, Object> columns = new LinkedHashMap<>();

    public static Row of(Object... namesAndValues) {
        Row row = new Row();
        for (int i = 0; i < namesAndValues.length; i += 2) {
            row.columns.put((String) namesAndValues[i], namesAndValues[i + 1]);
        }
        return row;
    }

    public Row copy() {
        Row copy = new Row();
        copy.columns.putAll(columns);
        return copy;
    }

    public Object get(String column) {
        return columns.get(column);
    }

    public String text(String column) {
        return (String) columns.get(column);
    }

    public int number(String column) {
        return (Integer) columns.get(column);
    }

    public Map<String, Object> columns() {
        return columns;
    }

    @Override
    public String toString() {
        return columns.toString();
    }
}
