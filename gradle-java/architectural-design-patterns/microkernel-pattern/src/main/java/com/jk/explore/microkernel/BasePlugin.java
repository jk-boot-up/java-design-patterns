package com.jk.explore.microkernel;

public abstract class BasePlugin implements Plugin {

    private final String name;
    private boolean running;

    protected BasePlugin(String name) {
        this.name = name;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public void start() {
        running = true;
    }

    @Override
    public void stop() {
        running = false;
    }

    public boolean running() {
        return running;
    }
}
