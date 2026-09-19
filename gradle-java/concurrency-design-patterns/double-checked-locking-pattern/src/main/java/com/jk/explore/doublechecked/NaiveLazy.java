package com.jk.explore.doublechecked;

/** Lazy creation with no protection: check, then create. Two threads can both pass the check. */
public class NaiveLazy {

    private static PriceList instance;

    private NaiveLazy() {
    }

    public static PriceList get() {
        if (instance == null) {
            Rendezvous.meet();
            instance = new PriceList();
        }
        return instance;
    }

    public static void reset() {
        instance = null;
    }
}
