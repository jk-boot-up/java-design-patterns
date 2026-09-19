package com.jk.explore.fluent;

import java.util.List;

/** A fluent query that changes itself and returns itself. Reads the same, behaves differently. */
public class MutableQuery {

    private Query inner = Query.search();

    public MutableQuery category(String category) {
        inner = inner.category(category);
        return this;
    }

    public MutableQuery under(int cents) {
        inner = inner.under(cents);
        return this;
    }

    public List<String> run() {
        return inner.run();
    }
}
