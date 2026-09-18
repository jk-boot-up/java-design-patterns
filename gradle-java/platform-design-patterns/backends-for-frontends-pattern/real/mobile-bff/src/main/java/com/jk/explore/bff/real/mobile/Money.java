package com.jk.explore.bff.real.mobile;

/**
 * Pence in, pounds out.
 *
 * <p>The shop's pricing service returns 4799. The decision to write that as "£47.99"
 * belongs to whoever is drawing the screen, and this is where it happens: in a process
 * the phone team can correct this afternoon, rather than inside an app that customers
 * will still be running in two years.
 */
public final class Money {

    private Money() {
    }

    public static String format(int pence) {
        return "£" + pence / 100 + "." + String.format("%02d", pence % 100);
    }
}
