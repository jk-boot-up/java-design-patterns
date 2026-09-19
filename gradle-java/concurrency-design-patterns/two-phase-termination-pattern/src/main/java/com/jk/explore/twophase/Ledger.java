package com.jk.explore.twophase;

import java.util.ArrayList;
import java.util.List;

/** Where orders are written, a line at a time. It can be closed, and it remembers if it was ever left with an order half written. */
public class Ledger {

    private final List<String> lines = new ArrayList<>();
    private boolean closed;
    private boolean inOrder;
    private boolean leftHalfWritten;

    public synchronized void begin() {
        inOrder = true;
    }

    public synchronized void writeLine(String line) {
        if (closed) {
            leftHalfWritten = inOrder;
            throw new IllegalStateException("the ledger is closed");
        }
        lines.add(line);
    }

    public synchronized void end() {
        inOrder = false;
    }

    public synchronized void close() {
        closed = true;
    }

    public synchronized List<String> lines() {
        return new ArrayList<>(lines);
    }

    public synchronized boolean leftHalfWritten() {
        return leftHalfWritten;
    }
}
