package com.jk.explore.frontcontroller;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

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
