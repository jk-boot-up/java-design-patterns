package com.jk.explore.onion.infrastructure;

public class SqlDatabase {

    private int statements;

    public void execute(String sql) {
        statements++;
    }

    public int statements() {
        return statements;
    }
}
