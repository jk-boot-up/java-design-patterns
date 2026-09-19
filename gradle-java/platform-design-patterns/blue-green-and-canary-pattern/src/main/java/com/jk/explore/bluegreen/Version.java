package com.jk.explore.bluegreen;

/** One release of the checkout service. A buggy release fails on orders of 100 pounds or more. */
public class Version {

    private final String name;
    private final boolean buggy;
    private final String format;
    private int served;
    private int failed;

    private Version(String name, boolean buggy, String format) {
        this.name = name;
        this.buggy = buggy;
        this.format = format;
    }

    public static Version good(String name) {
        return new Version(name, false, name);
    }

    public static Version buggy(String name) {
        return new Version(name, true, name);
    }

    public String name() {
        return name;
    }

    /** The format this release writes orders in. A different release may not be able to read it. */
    public String format() {
        return format;
    }

    public boolean handle(long cents) {
        served++;
        if (buggy && cents >= 10000) {
            failed++;
            return false;
        }
        return true;
    }

    public int served() {
        return served;
    }

    public int failed() {
        return failed;
    }

    public void resetCounts() {
        served = 0;
        failed = 0;
    }
}
