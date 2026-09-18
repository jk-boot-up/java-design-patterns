package com.jk.explore.bff.real.mobile;

/**
 * How a discount is written down for a customer — the phone team's copy.
 *
 * <p>This file is duplicated, almost but not quite, in {@code web-bff}. That
 * duplication is not an accident of the demo and it is not something to tidy up before
 * reading on: it is the failure the last act of this walkthrough exists to show, and
 * putting it in a shared module would be a different project teaching a different
 * lesson.
 *
 * <p>What a shop may claim a customer is saving is a matter of law in most countries,
 * and the rule has edges. The higher price has to have been the real price recently.
 * The version below was written before the pricing team added that condition, and it
 * was correct on the day it was written. It is well named. It has a test. The test
 * passes. It is wrong only in relation to a decision taken somewhere else, months
 * later, by people who had no reason to know this second copy existed — and there is no
 * test writable inside this process that could notice.
 */
public final class SavingRules {

    private SavingRules() {
    }

    /**
     * The copy taken before the review, still running.
     *
     * <p>Note what is missing rather than what is here: the {@code
     * listPriceHeldLongEnough} flag arrives on every pricing response this backend
     * fetches, and this method does not take it as an argument at all.
     */
    public static String savingLabel(int listPence, int nowPence) {
        return "Save " + Money.format(listPence - nowPence);
    }
}
