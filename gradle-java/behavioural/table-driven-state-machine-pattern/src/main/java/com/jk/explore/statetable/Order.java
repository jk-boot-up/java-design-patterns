package com.jk.explore.statetable;

import java.util.ArrayList;
import java.util.List;

/**
 * An order whose status only changes by looking the move up in the table.
 */
public final class Order {

    private final String id;
    private final TransitionTable table;
    private Status status = Status.PLACED;
    private final List<Status> history = new ArrayList<>(List.of(Status.PLACED));

    public Order(String id, TransitionTable table) {
        this.id = id;
        this.table = table;
    }

    public Order apply(Action action) {
        status = table.next(status, action).orElseThrow(() -> new IllegalStateException(
                "cannot " + action.name().toLowerCase() + " a " + status + " order"));
        history.add(status);
        return this;
    }

    public Status status() {
        return status;
    }

    public List<Status> history() {
        return List.copyOf(history);
    }

    public String id() {
        return id;
    }
}
