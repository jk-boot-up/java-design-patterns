package com.jk.explore.bff.real.web;

/**
 * How a discount is written down for a customer — the desktop team's copy.
 *
 * <p>This is the version that was updated when the pricing team finished their review,
 * and it has two conditions the phone's copy does not. The higher price must have been
 * genuinely in force long enough to be quoted against, and the saving must be at least
 * five per cent, because anything less reads as a trick.
 *
 * <p>Nobody did anything wrong to end up with the two out of step. The desktop team
 * were told about the review and acted on it. The phone team were not told, because
 * nobody knew there was a second copy to tell them about. That is the shape of this
 * failure every time it happens: not carelessness, but a decision that had no way of
 * reaching everywhere it applied.
 */
public final class SavingRules {

    private SavingRules() {
    }

    public static String savingLabel(int listPence, int nowPence, boolean listPriceHeldLongEnough) {
        if (!listPriceHeldLongEnough) {
            return "";
        }
        int savedPence = listPence - nowPence;
        int percent = (savedPence * 100) / listPence;
        if (percent < 5) {
            return "";
        }
        return "Save " + Money.format(savedPence) + " (" + percent + "%)";
    }
}
