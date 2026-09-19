package com.jk.explore.acl.adapter;

import com.jk.explore.acl.domain.Availability;
import com.jk.explore.acl.domain.InventoryGateway;
import com.jk.explore.acl.domain.StockLevel;
import com.jk.explore.acl.legacy.LegacyInventorySystem;
import com.jk.explore.acl.legacy.LegacyStockRecord;

/**
 * The anti-corruption layer. It is the only class that knows the legacy system's codes. It
 * translates in one direction, refuses what it cannot translate, and keeps every "Y", "D" and
 * "0012" from reaching the rest of the shop.
 */
public class LegacyInventoryAdapter implements InventoryGateway {

    private final LegacyInventorySystem legacy;

    public LegacyInventoryAdapter(LegacyInventorySystem legacy) {
        this.legacy = legacy;
    }

    @Override
    public StockLevel stockOf(String sku) {
        LegacyStockRecord row = legacy.fetch(sku);
        if (row == null) {
            throw new UntranslatableLegacyData(sku, "no such item");
        }
        int quantity;
        try {
            quantity = Integer.parseInt(row.QTY_ON_HND().trim());
        } catch (NumberFormatException e) {
            throw new UntranslatableLegacyData(sku, "quantity '" + row.QTY_ON_HND() + "' is not a number");
        }
        return new StockLevel(sku, quantity, availability(sku, row));
    }

    private static Availability availability(String sku, LegacyStockRecord row) {
        return switch (row.ITM_STAT()) {
            case "D" -> Availability.DISCONTINUED;
            case "H" -> Availability.ON_HOLD;
            case "A", "S" -> "Y".equals(row.IN_STK_FLG()) ? Availability.IN_STOCK : Availability.OUT_OF_STOCK;
            default -> throw new UntranslatableLegacyData(sku, "status '" + row.ITM_STAT() + "' is not known");
        };
    }

    /** The fields the legacy system sends and the shop does not use. Listed so that dropping them is a decision. */
    public static java.util.List<String> fieldsDropped() {
        return java.util.List.of("LST_CNT_DT", "WHSE_CD", "UOM");
    }
}
