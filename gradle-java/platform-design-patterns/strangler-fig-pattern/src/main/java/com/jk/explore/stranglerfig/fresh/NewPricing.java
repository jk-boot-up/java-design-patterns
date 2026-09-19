package com.jk.explore.stranglerfig.fresh;

import com.jk.explore.stranglerfig.domain.Order;
import com.jk.explore.stranglerfig.domain.Pricer;
import com.jk.explore.stranglerfig.domain.Pricing;

/**
 * <strong>The rewritten pricing.</strong> Written from the business rules as people
 * described them, so it rounds VAT once on the total and makes delivery free from
 * fifty pounds up. Both are reasonable, and both differ from what the legacy code
 * has actually charged for years. Shadow reads find that out before a customer does.
 */
public class NewPricing implements Pricer {

    private final boolean matchLegacy;

    /** @param matchLegacy after the differences are understood, reproduce the legacy behaviour exactly */
    public NewPricing(boolean matchLegacy) {
        this.matchLegacy = matchLegacy;
    }

    @Override
    public Pricing price(Order order) {
        long subtotal = order.subtotalPence();
        long vat;
        if (matchLegacy) {
            vat = order.lines().stream().mapToLong(l -> (l.linePence() * 20 + 50) / 100).sum();
        } else {
            vat = (subtotal * 20 + 50) / 100;
        }
        boolean free = matchLegacy ? subtotal > 5_000 : subtotal >= 5_000;
        long delivery = free ? 0 : 495;
        return new Pricing(subtotal, vat, delivery, subtotal + vat + delivery);
    }
}
