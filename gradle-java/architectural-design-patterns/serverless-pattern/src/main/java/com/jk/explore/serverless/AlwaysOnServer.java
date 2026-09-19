package com.jk.explore.serverless;

/** The version with a machine that runs all the time and is paid for all the time. */
public class AlwaysOnServer {

    private final int costPerTick;

    public AlwaysOnServer(int costPerTick) {
        this.costPerTick = costPerTick;
    }

    public int bill(int ticks) {
        return ticks * costPerTick;
    }
}
