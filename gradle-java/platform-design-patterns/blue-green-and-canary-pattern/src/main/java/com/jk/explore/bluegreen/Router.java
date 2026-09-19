package com.jk.explore.bluegreen;

/** Sends each request to blue or to green, by a fixed rule, so runs are repeatable. */
public class Router {

    private final Version blue;
    private final Version green;
    private int greenPercent;
    private int lost;

    public Router(Version blue, Version green) {
        this.blue = blue;
        this.green = green;
    }

    public void setGreenPercent(int percent) {
        this.greenPercent = percent;
    }

    public int greenPercent() {
        return greenPercent;
    }

    /** Request number seq goes to green when seq mod 100 is below the green share. */
    public boolean route(int seq, long cents) {
        Version target = seq % 100 < greenPercent ? green : blue;
        boolean ok = target.handle(cents);
        if (!ok) {
            lost++;
        }
        return ok;
    }

    public int failures() {
        return lost;
    }

    public Version blue() {
        return blue;
    }

    public Version green() {
        return green;
    }

    /** Ten in a hundred requests are big orders. */
    public static long orderCents(int seq) {
        return seq % 10 == 0 ? 12000 : 2000;
    }
}
