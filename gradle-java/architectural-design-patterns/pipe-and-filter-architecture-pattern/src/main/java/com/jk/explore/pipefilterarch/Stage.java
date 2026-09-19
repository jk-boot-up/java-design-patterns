package com.jk.explore.pipefilterarch;

/** One stage: a waiting line in front of some workers, each taking a fixed number of ticks per order. */
public class Stage {

    private final String name;
    private final int cost;
    private final int limit;
    private final int[] left;
    private final boolean[] holding;
    private int queue;
    private int peakQueue;

    public Stage(String name, int cost, int workers, int queueLimit) {
        this.name = name;
        this.cost = cost;
        this.limit = queueLimit;
        this.left = new int[workers];
        this.holding = new boolean[workers];
    }

    public String name() {
        return name;
    }

    public int queued() {
        return queue;
    }

    public int peakQueue() {
        return peakQueue;
    }

    public boolean accept() {
        if (queue >= limit) {
            return false;
        }
        queue++;
        peakQueue = Math.max(peakQueue, queue);
        return true;
    }

    /** Orders in this stage: waiting, being worked on, or held because the next stage is full. */
    public int inFlight() {
        int n = queue;
        for (int w = 0; w < left.length; w++) {
            if (left[w] > 0 || holding[w]) {
                n++;
            }
        }
        return n;
    }

    public int crash() {
        int lost = inFlight();
        queue = 0;
        for (int w = 0; w < left.length; w++) {
            left[w] = 0;
            holding[w] = false;
        }
        return lost;
    }

    /** One tick. Returns how many orders left this stage. */
    int advance(Stage next) {
        int finished = 0;
        for (int w = 0; w < left.length; w++) {
            boolean ready = false;
            if (holding[w]) {
                ready = true;
            } else if (left[w] > 0 && --left[w] == 0) {
                ready = true;
            }
            if (ready) {
                if (next == null || next.accept()) {
                    holding[w] = false;
                    finished++;
                } else {
                    holding[w] = true;
                }
            }
            if (left[w] == 0 && !holding[w] && queue > 0) {
                queue--;
                left[w] = cost;
            }
        }
        return finished;
    }
}
