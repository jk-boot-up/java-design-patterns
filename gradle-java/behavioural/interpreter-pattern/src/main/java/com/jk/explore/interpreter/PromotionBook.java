package com.jk.explore.interpreter;

import java.util.ArrayList;
import java.util.List;

/**
 * Every promotion the shop is running, and the one thing the checkout asks it.
 *
 * <p>Read this class looking for what it does <em>not</em> contain. There is no
 * mention of countries, baskets, item counts or first orders anywhere in it. It
 * asks each promotion whether it applies and keeps the best answer, and it
 * would still be correct if marketing invented a rule nobody has thought of
 * yet.
 */
public class PromotionBook {

    private final List<Promotion> promotions = new ArrayList<>();

    /** Reads the promotions as written; a bad line stops it here, loudly. */
    public static PromotionBook fromLines(List<String> lines) {
        PromotionBook book = new PromotionBook();
        for (String line : lines) {
            book.promotions.add(Promotion.fromLine(line));
        }
        return book;
    }

    public List<Promotion> promotions() {
        return List.copyOf(promotions);
    }

    /**
     * The best discount this order qualifies for, as a percentage, or 0.
     *
     * <p>Ties go to whichever was written first, which is a business decision
     * rather than a technical one — and it is made here, once, rather than
     * being an accident of the order of a {@code switch}.
     */
    public int bestPercentFor(Order order) {
        int best = 0;
        for (Promotion promotion : promotions) {
            if (promotion.appliesTo(order) && promotion.percentOff() > best) {
                best = promotion.percentOff();
            }
        }
        return best;
    }

    /** Which promotions matched, for the audit log and for the shopper. */
    public List<String> reasonsFor(Order order) {
        List<String> reasons = new ArrayList<>();
        for (Promotion promotion : promotions) {
            if (promotion.appliesTo(order)) {
                reasons.add(promotion.explain());
            }
        }
        return reasons;
    }
}
