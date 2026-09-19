package com.jk.explore.acl.naive;

import com.jk.explore.acl.legacy.LegacyStockRecord;

/**
 * The shop using the legacy record directly. Four features, and each has learnt the codes for itself.
 * When the legacy system adds a status, each of them decides on its own what an unknown one means.
 */
public final class NaiveShop {

    private NaiveShop() {
    }

    public static String productPageLabel(LegacyStockRecord r) {
        if ("D".equals(r.ITM_STAT())) {
            return "discontinued";
        }
        return "Y".equals(r.IN_STK_FLG()) ? "in stock" : "out of stock";
    }

    public static boolean canAddToBasket(LegacyStockRecord r) {
        return "Y".equals(r.IN_STK_FLG()) && !"D".equals(r.ITM_STAT());
    }

    public static int reorderQuantity(LegacyStockRecord r) {
        return "A".equals(r.ITM_STAT()) ? Math.max(0, 50 - Integer.parseInt(r.QTY_ON_HND())) : 0;
    }

    public static String reportLine(LegacyStockRecord r) {
        return r.ITM_CD() + " " + Integer.parseInt(r.QTY_ON_HND()) + " " + r.ITM_STAT();
    }

    public static int placesThatKnowTheCodes() {
        int n = 0;
        for (var m : NaiveShop.class.getDeclaredMethods()) {
            if (m.getParameterCount() == 1 && m.getParameterTypes()[0] == LegacyStockRecord.class) {
                n++;
            }
        }
        return n;
    }
}
