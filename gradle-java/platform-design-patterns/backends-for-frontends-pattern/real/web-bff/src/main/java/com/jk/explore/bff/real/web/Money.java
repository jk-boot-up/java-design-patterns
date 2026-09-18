package com.jk.explore.bff.real.web;

/**
 * Pence in, pounds out.
 *
 * <p>A second copy of the same four lines, and this one is genuinely fine. Formatting
 * money for a screen is presentation, which is the one thing a backend for a frontend
 * is supposed to own, so two backends holding two copies of it is two teams each owning
 * their own presentation rather than one rule living in two places.
 *
 * <p>Compare it with {@link SavingRules} next door, which is the same shape of
 * duplication and is not fine at all. The difference is not how much code there is. It
 * is whether the shop would still believe the thing with every client switched off.
 */
public final class Money {

    private Money() {
    }

    public static String format(int pence) {
        return "£" + pence / 100 + "." + String.format("%02d", pence % 100);
    }
}
