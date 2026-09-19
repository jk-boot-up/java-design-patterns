package com.jk.explore.microkernel;

public class BrokenPlugin extends BasePlugin {

    public BrokenPlugin(String name) {
        super(name);
    }

    @Override
    public long adjust(long cents) {
        throw new IllegalStateException(name() + " lost its connection");
    }
}
