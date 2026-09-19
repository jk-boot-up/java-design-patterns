package com.jk.explore.activerecord;

import java.util.HashMap;
import java.util.Map;

/** An active record: one row of the customers table, that knows how to find and save itself. */
public class Customer {

    static final Table TABLE = new Table();

    private Integer id;
    private final String name;

    public Customer(String name) {
        this.name = name;
    }

    public Integer id() {
        return id;
    }

    public String name() {
        return name;
    }

    public Customer save() {
        Map<String, Object> row = new HashMap<>();
        row.put("name", name);
        if (id == null) {
            id = TABLE.insert(row);
        } else {
            TABLE.update(id, row);
        }
        return this;
    }

    public static Customer find(int id) {
        Map<String, Object> row = TABLE.find(id);
        Customer c = new Customer((String) row.get("name"));
        c.id = id;
        return c;
    }
}
