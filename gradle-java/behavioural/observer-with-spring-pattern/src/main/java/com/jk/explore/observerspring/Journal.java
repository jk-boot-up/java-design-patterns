package com.jk.explore.observerspring;

import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Where listeners write what they did, so the demo and the tests can read it back. */
@Component
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

    public void clear() {
        lines.clear();
    }
}
