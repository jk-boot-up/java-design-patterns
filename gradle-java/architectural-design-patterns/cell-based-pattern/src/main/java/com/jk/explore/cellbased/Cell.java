package com.jk.explore.cellbased;

import java.util.ArrayList;
import java.util.List;

/**
 * A complete copy of the shop's back end (checkout, orders, its own database) serving only the customers placed in it.
 */
public final class Cell {

    private final String name;
    private final List<String> orders = new ArrayList<>();
    private String release = "v1";

    public Cell(String name) {
        this.name = name;
    }

    public String checkout(String customerId, long pence) {
        if (release.equals("v2-buggy")) {
            throw new IllegalStateException("checkout crashed in " + name);
        }
        orders.add(customerId + ":" + pence);
        return "order placed in " + name;
    }

    public void deploy(String release) {
        this.release = release;
    }

    public long salesPence() {
        return orders.stream().mapToLong(o -> Long.parseLong(o.split(":")[1])).sum();
    }

    public String name() {
        return name;
    }

    public String release() {
        return release;
    }
}
