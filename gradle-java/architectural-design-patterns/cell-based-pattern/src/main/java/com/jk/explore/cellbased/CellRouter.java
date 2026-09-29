package com.jk.explore.cellbased;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * The pattern's thin front door: knows which cell each customer lives in, and sends every request there.
 *
 * <p>Existing customers are placed once and stay put. New customers go
 * wherever the router is told to place them, which is how a new cell is
 * filled without moving anyone.
 */
public final class CellRouter {

    private final List<Cell> cells = new ArrayList<>();
    private final Map<String, Cell> placement = new HashMap<>();
    private Cell newCustomersGoTo;

    public void addCell(Cell cell) {
        cells.add(cell);
    }

    /** Spread existing customers evenly across the current cells. */
    public void place(List<String> customers) {
        for (int i = 0; i < customers.size(); i++) {
            placement.put(customers.get(i), cells.get(i % cells.size()));
        }
    }

    public void sendNewCustomersTo(Cell cell) {
        newCustomersGoTo = cell;
    }

    public Cell cellOf(String customer) {
        return placement.computeIfAbsent(customer, c -> newCustomersGoTo);
    }

    public String checkout(String customer, long pence) {
        return cellOf(customer).checkout(customer, pence);
    }

    public List<Cell> cells() {
        return cells;
    }
}
