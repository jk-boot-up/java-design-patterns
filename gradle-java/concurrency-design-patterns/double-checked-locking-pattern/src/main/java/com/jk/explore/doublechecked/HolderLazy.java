package com.jk.explore.doublechecked;

/**
 * The simplest correct way. The JVM initialises a class the first time it is used, and does it once, under its own
 * lock. The holder is not touched until get() is called, so the price list is lazy, and no lock or volatile is written here.
 */
public final class HolderLazy {

    private HolderLazy() {
    }

    private static final class Holder {
        static final PriceList INSTANCE = new PriceList();
    }

    public static PriceList get() {
        return Holder.INSTANCE;
    }
}
