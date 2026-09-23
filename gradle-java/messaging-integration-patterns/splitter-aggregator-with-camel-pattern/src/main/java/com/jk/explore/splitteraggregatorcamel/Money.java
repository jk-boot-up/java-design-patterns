package com.jk.explore.splitteraggregatorcamel;

/** Turns a whole number of pence into the text a customer reads. */
public final class Money {

    private Money() {
    }

    public static String pounds(int pence) {
        return "£" + (pence / 100) + "." + String.format("%02d", pence % 100);
    }
}
