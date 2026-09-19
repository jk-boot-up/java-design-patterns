package com.jk.explore.sidecarkubernetes;

/** A running container: the thing the manifest described, with a life of its own. */
public final class Container {

    private final ContainerSpec spec;
    private boolean running = true;
    private int restarts;
    private int starts = 1;

    Container(ContainerSpec spec) {
        this.spec = spec;
    }

    public ContainerSpec spec() {
        return spec;
    }

    public String name() {
        return spec.name();
    }

    public boolean running() {
        return running;
    }

    /** How many times the kubelet has restarted <em>this container</em>. */
    public int restarts() {
        return restarts;
    }

    /** How many times this container has been started, including the first time. */
    public int starts() {
        return starts;
    }

    void crash() {
        running = false;
    }

    void restart() {
        running = true;
        restarts++;
        starts++;
    }
}
