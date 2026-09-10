package com.jk.explore.interpreter;

/**
 * The trap: every promotion written straight into Java, as a branch.
 *
 * <p>This is the obvious way, and for the first promotion it is genuinely the
 * right way. The trouble arrives with the fourth. Each branch is a copy of the
 * one above it with the numbers changed, and a copy is exactly the kind of
 * thing a hurried person gets almost right.
 *
 * <p>There are two mistakes in here — one condition that was never written and
 * one that was copied in from a promotion that ended last spring — and neither
 * throws anything. Do not fix them: {@code NaiveVoucherRulesTest} pins both in
 * place on purpose, so that the cost of writing rules this way is something the
 * build states out loud rather than something a README claims.
 */
public class NaiveVoucherRules {

    /** The best discount for an order, as a percentage. */
    public int bestPercentFor(Order order) {
        int best = 0;
        best = Math.max(best, save10(order));
        best = Math.max(best, save15(order));
        best = Math.max(best, freeship(order));
        return best;
    }

    /** SAVE10 — a UK order over £50. This one is correct. */
    private int save10(Order order) {
        if ("UK".equals(order.country()) && order.basketPounds() > 50) {
            return 10;
        }
        return 0;
    }

    /**
     * SAVE15 — meant to be a UK order over £100.
     *
     * <p>The ticket said "fifteen percent on baskets over one hundred". That
     * the offer was UK-only was in the paragraph above the sentence somebody
     * read, so no line of code was ever written for it. Every large overseas
     * order now takes fifteen percent off, and nothing anywhere complains.
     */
    private int save15(Order order) {
        if (order.basketPounds() > 100) {
            return 15;
        }
        return 0;
    }

    /**
     * FREESHIP — meant to be a UK order of three items or more.
     *
     * <p>It was copied from a welcome offer that retired last spring, and the
     * first-order check came with it. Returning shoppers quietly get nothing,
     * which nobody notices because a missing discount looks like a shopper who
     * did not qualify.
     */
    private int freeship(Order order) {
        if (order.firstOrder() && "UK".equals(order.country()) && order.itemCount() >= 3) {
            return 5;
        }
        return 0;
    }
}
