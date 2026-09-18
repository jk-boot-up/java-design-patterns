package com.jk.explore.sidecarjavaproxy;

/** Pence in, pounds out, with two decimal places and a pound sign. */
public final class Money {

    private Money() {
    }

    public static String format(int pence) {
        return "£" + pence / 100 + "." + String.format("%02d", Math.abs(pence % 100));
    }
}
