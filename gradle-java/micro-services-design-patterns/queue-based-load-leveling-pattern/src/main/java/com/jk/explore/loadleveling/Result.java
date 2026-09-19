package com.jk.explore.loadleveling;

/** What a run of the simulation ended up with. All counts, no clocks: one tick is one step of the model. */
public record Result(int arrived, int processed, int rejected, int lost, int maxDepth, int maxWaitTicks, double averageWaitTicks, int leftInQueue) {
}
