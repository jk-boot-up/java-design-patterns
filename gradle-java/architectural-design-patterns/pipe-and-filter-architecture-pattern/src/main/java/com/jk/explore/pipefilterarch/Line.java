package com.jk.explore.pipefilterarch;

import java.util.List;

/** Stages joined by waiting lines. Orders go in at the front and come out at the end. */
public class Line {

    private final List<Stage> stages;
    private int out;
    private int refused;

    public Line(Stage... stages) {
        this.stages = List.of(stages);
    }

    /** One tick: the last stage first, so room made at the end is seen by the stages before it. */
    public void tick(boolean anOrderArrives) {
        for (int i = stages.size() - 1; i >= 0; i--) {
            Stage next = i + 1 < stages.size() ? stages.get(i + 1) : null;
            int finished = stages.get(i).advance(next);
            if (next == null) {
                out += finished;
            }
        }
        if (anOrderArrives && !stages.get(0).accept()) {
            refused++;
        }
    }

    public void run(int ticks) {
        for (int t = 0; t < ticks; t++) {
            tick(true);
        }
    }

    public int out() {
        return out;
    }

    public int refused() {
        return refused;
    }

    public Stage stage(String name) {
        return stages.stream().filter(s -> s.name().equals(name)).findFirst().orElseThrow();
    }

    public List<Stage> stages() {
        return stages;
    }
}
