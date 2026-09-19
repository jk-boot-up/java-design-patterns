package com.jk.explore.nullobject.pattern;

import com.jk.explore.nullobject.domain.Discount;
import com.jk.explore.nullobject.domain.DiscountDirectory;
import com.jk.explore.nullobject.domain.DiscountServiceDown;

/**
 * <strong>The bill: a null object that hides an error.</strong> It turns a
 * failed lookup into "no discount", so a customer entitled to a discount is
 * charged full price and nothing anywhere says so.
 */
public class ForgivingDirectory {

    private final DiscountDirectory directory;

    public ForgivingDirectory(DiscountDirectory directory) {
        this.directory = directory;
    }

    public Discount find(int customerId) {
        try {
            Discount found = directory.find(customerId);
            return found == null ? NoDiscount.INSTANCE : found;
        } catch (DiscountServiceDown e) {
            return NoDiscount.INSTANCE;
        }
    }
}
