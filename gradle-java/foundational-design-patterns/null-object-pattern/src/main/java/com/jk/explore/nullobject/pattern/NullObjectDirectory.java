package com.jk.explore.nullobject.pattern;

import com.jk.explore.nullobject.domain.Discount;
import com.jk.explore.nullobject.domain.DiscountDirectory;

/** {@code find} never returns null: a missing discount is a {@link NoDiscount}. A service that is down still throws. */
public class NullObjectDirectory {

    private final DiscountDirectory directory;

    public NullObjectDirectory(DiscountDirectory directory) {
        this.directory = directory;
    }

    public Discount find(int customerId) {
        Discount found = directory.find(customerId);
        return found == null ? NoDiscount.INSTANCE : found;
    }
}
