package com.jk.explore.microkernel;

public class Fee extends BasePlugin {

    private final long cents;

    public Fee(String name, long cents) {
        super(name);
        this.cents = cents;
    }

    @Override
    public long adjust(long total) {
        return total + cents;
    }
}
