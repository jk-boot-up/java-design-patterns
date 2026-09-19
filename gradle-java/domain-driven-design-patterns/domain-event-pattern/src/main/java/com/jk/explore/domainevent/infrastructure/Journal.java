package com.jk.explore.domainevent.infrastructure;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Where the handlers write what they did, so a demo and a test can read it back. */
public class Journal {

    private final List<String> lines = Collections.synchronizedList(new ArrayList<>());

    public void add(String line) {
        lines.add(line);
    }

    public List<String> lines() {
        synchronized (lines) {
            return List.copyOf(lines);
        }
    }
}
