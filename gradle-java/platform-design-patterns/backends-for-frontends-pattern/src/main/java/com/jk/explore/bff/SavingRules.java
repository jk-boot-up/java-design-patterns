package com.jk.explore.bff;

/**
 * How a discount is written down for a customer.
 *
 * <p>This looks like a formatting detail and is not one. What a shop may claim a
 * customer is saving is a matter of law in most countries, and the rule has edges: the
 * higher price has to have been the real price recently, and a saving too small to
 * matter may not be advertised as a saving at all. A shop gets this wrong and it is a
 * letter from a regulator, not a bug report.
 *
 * <p>It is here because it is the classic thing that gets copied into two backends and
 * then changed in one of them. Act 5 is that story.
 */
public interface SavingRules {

    /** What the screen should say about the discount, or an empty string for nothing. */
    String savingLabel(int listPence, int nowPence, boolean listPriceHeldLongEnough);

    /**
     * The current rule, as it was rewritten after the pricing review.
     *
     * <p>Two conditions. The higher price must have been genuinely in force for long
     * enough to be quoted, and the saving must be at least five per cent, because
     * anything less reads as a trick.
     */
    static SavingRules current() {
        return (listPence, nowPence, listPriceHeldLongEnough) -> {
            if (!listPriceHeldLongEnough) {
                return "";
            }
            int savedPence = listPence - nowPence;
            int percent = (savedPence * 100) / listPence;
            if (percent < 5) {
                return "";
            }
            return "Save " + Money.format(savedPence) + " (" + percent + "%)";
        };
    }

    /**
     * The copy that was taken before the review and never caught up.
     *
     * <p>Nothing about it is careless. It was correct on the day it was written, it is
     * well named, it has tests, and those tests pass. It is wrong only in relation to a
     * decision made somewhere else, months later, by people who had no reason to know
     * this second copy existed.
     */
    static SavingRules copiedBeforeTheReview() {
        return (listPence, nowPence, listPriceHeldLongEnough) ->
                "Save " + Money.format(listPence - nowPence);
    }
}
