package com.jk.explore.templatemethod;

import java.util.HashSet;
import java.util.Set;

/**
 * A stand-in for a third-party marketplace seller's system. The store cannot
 * reserve their stock; it can only ask, and be told yes or no.
 */
public final class SellerApi {

    private final String sellerName;
    private final Set<String> confirmable = new HashSet<>();
    private int callCount;

    public SellerApi(String sellerName) {
        this.sellerName = sellerName;
    }

    public SellerApi willConfirm(String... skus) {
        confirmable.addAll(Set.of(skus));
        return this;
    }

    public String sellerName() {
        return sellerName;
    }

    public int callCount() {
        return callCount;
    }

    /** Asks the seller to commit to a line. Returns false if they will not. */
    public boolean confirm(String sku, int units) {
        callCount++;
        return confirmable.contains(sku);
    }
}
