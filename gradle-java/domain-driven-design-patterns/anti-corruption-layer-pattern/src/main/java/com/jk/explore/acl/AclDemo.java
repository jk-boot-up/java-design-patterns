package com.jk.explore.acl;

import com.jk.explore.acl.adapter.LegacyInventoryAdapter;
import com.jk.explore.acl.adapter.UntranslatableLegacyData;
import com.jk.explore.acl.domain.StockLevel;
import com.jk.explore.acl.legacy.LegacyInventorySystem;
import com.jk.explore.acl.legacy.LegacyStockRecord;
import com.jk.explore.acl.naive.NaiveShop;

import java.util.List;

public class AclDemo {

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. Their model, everywhere.");
        LegacyStockRecord row = new LegacyInventorySystem().fetch("MUG-BLUE");
        System.out.println("  what the old system sends: " + row + ".");
        System.out.println("  product page: " + NaiveShop.productPageLabel(row) + ". basket: " + NaiveShop.canAddToBasket(row)
                + ". reorder: " + NaiveShop.reorderQuantity(row) + ". report: " + NaiveShop.reportLine(row) + ".");
        System.out.println("  places in the shop that have learnt the codes Y, N, A, D and S: " + NaiveShop.placesThatKnowTheCodes() + ".");
    }

    private static void two() {
        System.out.println("TWO. Their model, translated once.");
        LegacyInventoryAdapter gateway = new LegacyInventoryAdapter(new LegacyInventorySystem());
        for (String sku : List.of("MUG-BLUE", "MUG-OLD", "TEA-050")) {
            StockLevel level = gateway.stockOf(sku);
            System.out.println("  " + level + ", can be bought: " + level.canBeBought() + ".");
        }
        System.out.println("  no code, and no string pretending to be a number, has crossed the layer.");
    }

    private static void three() {
        System.out.println("THREE. Bad data stops at the door.");
        LegacyInventorySystem legacy = new LegacyInventorySystem();
        legacy.corrupt("MUG-BLUE");
        try {
            NaiveShop.reportLine(legacy.fetch("MUG-BLUE"));
        } catch (NumberFormatException e) {
            System.out.println("  the shortcut, deep in a report: NumberFormatException, and no sku in the message.");
        }
        try {
            new LegacyInventoryAdapter(legacy).stockOf("MUG-BLUE");
        } catch (UntranslatableLegacyData e) {
            System.out.println("  the layer: " + e.getMessage() + ".");
        }
    }

    private static void four() {
        System.out.println("FOUR. The other side changes.");
        LegacyInventorySystem legacy = new LegacyInventorySystem();
        legacy.putOnHold("TEA-050");
        LegacyStockRecord row = legacy.fetch("TEA-050");
        System.out.println("  the old system starts sending status H for a product on hold.");
        System.out.println("  the shortcut: page says " + NaiveShop.productPageLabel(row) + ", basket allows it: " + NaiveShop.canAddToBasket(row)
                + ", reorder: " + NaiveShop.reorderQuantity(row) + ". four places, four private guesses.");
        StockLevel level = new LegacyInventoryAdapter(legacy).stockOf("TEA-050");
        System.out.println("  the layer: " + level.availability() + ", can be bought: " + level.canBeBought() + ". one decision, in one place.");
    }

    private static void five() {
        System.out.println("FIVE. What the layer costs.");
        System.out.println("  the old row has 7 fields. the shop uses 4 of them. the layer drops: " + LegacyInventoryAdapter.fieldsDropped() + ".");
        System.out.println("  the day a feature needs the last count date, the layer must be extended, and the shop's model with it.");
    }

    private static void six() {
        System.out.println("SIX. What the layer protects.");
        System.out.println("  the shop's own words: " + java.util.Arrays.toString(com.jk.explore.acl.domain.Availability.values()) + ".");
        System.out.println("  the old system's words stay behind the layer. replace the old system, write one new adapter, and nothing else changes.");
    }
}
