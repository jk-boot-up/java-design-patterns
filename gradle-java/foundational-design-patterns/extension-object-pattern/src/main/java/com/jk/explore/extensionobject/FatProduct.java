package com.jk.explore.extensionobject;

import java.lang.reflect.RecordComponent;

/**
 * Without the pattern: one product class with a field for every feature any product has ever needed.
 *
 * <p>A mug leaves most of them empty, and every new feature means editing
 * this class, which the whole shop depends on.
 */
public record FatProduct(String sku, String name, Long pricePence,
                         String downloadUrl, Integer maxDownloads,
                         Integer warrantyYears,
                         Boolean giftWrap,
                         Integer ageLimit) {

    /** How many of the fields are empty. */
    public int emptyFields() {
        int n = 0;
        for (RecordComponent c : getClass().getRecordComponents()) {
            try {
                if (c.getAccessor().invoke(this) == null) {
                    n++;
                }
            } catch (ReflectiveOperationException e) {
                throw new IllegalStateException(e);
            }
        }
        return n;
    }

    public int fields() {
        return getClass().getRecordComponents().length;
    }
}
