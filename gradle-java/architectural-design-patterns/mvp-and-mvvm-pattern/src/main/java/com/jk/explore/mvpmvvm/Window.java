package com.jk.explore.mvpmvvm;

/** Stands for a real screen: opening one is slow and needs a display. */
public class Window {

    private static int opened;

    public Window() {
        opened++;
    }

    public static int opened() {
        return opened;
    }

    public static void reset() {
        opened = 0;
    }
}
