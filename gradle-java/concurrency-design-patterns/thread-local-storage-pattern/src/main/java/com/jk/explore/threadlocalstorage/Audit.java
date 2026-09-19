package com.jk.explore.threadlocalstorage;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** The audit log, written deep in the code. It records who did what. */
public class Audit {

    private final List<String> lines = Collections.synchronizedList(new ArrayList<>());

    /** With the customer passed in by every caller above it. */
    public void recordExplicit(String customer, String action) {
        lines.add(customer + ": " + action);
    }

    /** With the customer found from the current thread's context. */
    public void record(String action) {
        lines.add(RequestContext.customer() + ": " + action);
    }

    public List<String> lines() {
        synchronized (lines) {
            return new ArrayList<>(lines);
        }
    }
}
