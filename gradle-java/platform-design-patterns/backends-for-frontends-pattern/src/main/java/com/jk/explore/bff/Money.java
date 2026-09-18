package com.jk.explore.bff;

/**
 * Pence in, pounds out.
 *
 * <p>Prices are held as whole pence everywhere in this project and formatted at the
 * last possible moment. That is the ordinary discipline for money in any language with
 * floating point in it, and here it also carries a point about the pattern: the shop's
 * pricing service returns 4799, and the decision to write that as "£47.99" belongs to
 * whoever is drawing the screen, not to whoever owns the number.
 */
public final class Money {

    private Money() {
    }

    public static String format(int pence) {
        return "£" + pence / 100 + "." + String.format("%02d", pence % 100);
    }
}
