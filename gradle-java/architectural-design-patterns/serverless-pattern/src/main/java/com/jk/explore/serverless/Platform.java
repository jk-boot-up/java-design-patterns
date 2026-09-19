package com.jk.explore.serverless;

import java.util.ArrayList;
import java.util.List;

/**
 * A tiny stand-in for a function platform, run on a counted clock. It starts an instance when a call
 * needs one, keeps it warm for a while, and throws it away when it has been idle too long.
 */
public class Platform {

    private static class Instance {
        int uses;
        int lastUsed;
    }

    private final int coldStartTicks;
    private final int idleTimeout;
    private final int maxDuration;
    private final List<Instance> instances = new ArrayList<>();
    private int now;
    private int invocations;
    private int coldStarts;
    private int latency;
    private int sharedCount;
    private int lastInstanceUses;

    public Platform(int coldStartTicks, int idleTimeout, int maxDuration) {
        this.coldStartTicks = coldStartTicks;
        this.idleTimeout = idleTimeout;
        this.maxDuration = maxDuration;
    }

    /** Runs n calls at the same moment. Each needs its own instance. */
    public void invoke(int n) {
        List<Instance> busy = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            Instance chosen = null;
            for (Instance inst : instances) {
                if (!busy.contains(inst)) {
                    chosen = inst;
                    break;
                }
            }
            if (chosen == null) {
                chosen = new Instance();
                instances.add(chosen);
                coldStarts++;
                latency += coldStartTicks;
            }
            busy.add(chosen);
            chosen.uses++;
            chosen.lastUsed = now;
            lastInstanceUses = chosen.uses;
            sharedCount++;
            invocations++;
        }
    }

    public void advance(int ticks) {
        now += ticks;
        instances.removeIf(i -> now - i.lastUsed >= idleTimeout);
    }

    /** Returns true if the work finished, false if the platform stopped it at the time limit. */
    public boolean runWork(int workTicks) {
        invoke(1);
        return workTicks <= maxDuration;
    }

    public int instances() {
        return instances.size();
    }

    public int invocations() {
        return invocations;
    }

    public int coldStarts() {
        return coldStarts;
    }

    public int latency() {
        return latency;
    }

    /** What the last instance used remembers in its own memory. */
    public int lastInstanceUses() {
        return lastInstanceUses;
    }

    /** What an outside store, which outlives every instance, remembers. */
    public int sharedCount() {
        return sharedCount;
    }

    public int bill(int pricePerInvocation) {
        return invocations * pricePerInvocation;
    }
}
