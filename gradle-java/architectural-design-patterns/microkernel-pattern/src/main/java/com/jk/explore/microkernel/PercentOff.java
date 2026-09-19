package com.jk.explore.microkernel;

public class PercentOff extends BasePlugin {

    private final int percent;

    public PercentOff(String name, int percent) {
        super(name);
        this.percent = percent;
    }

    @Override
    public long adjust(long cents) {
        return cents - cents * percent / 100;
    }
}
