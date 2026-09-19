package com.jk.explore.acl.legacy;

import java.util.HashMap;
import java.util.Map;

/**
 * The system we do not own and cannot change. Statuses are A (active), D (discontinued) and S (suspended).
 * One day its owners add H, for a product on hold, without telling anyone.
 */
public class LegacyInventorySystem {

    private final Map<String, LegacyStockRecord> rows = new HashMap<>();

    public LegacyInventorySystem() {
        rows.put("MUG-BLUE", new LegacyStockRecord("MUG-BLUE", "0012", "Y", "A", "20260114", "W01", "EA"));
        rows.put("MUG-OLD", new LegacyStockRecord("MUG-OLD", "0000", "N", "D", "20251201", "W01", "EA"));
        rows.put("TEA-050", new LegacyStockRecord("TEA-050", "0240", "Y", "A", "20260110", "W02", "EA"));
    }

    public LegacyStockRecord fetch(String sku) {
        return rows.get(sku);
    }

    /** The legacy owners' surprise: a status nobody was told about. */
    public void putOnHold(String sku) {
        LegacyStockRecord r = rows.get(sku);
        rows.put(sku, new LegacyStockRecord(r.ITM_CD(), r.QTY_ON_HND(), r.IN_STK_FLG(), "H", r.LST_CNT_DT(), r.WHSE_CD(), r.UOM()));
    }

    /** A record with a quantity that is not a number, which happens more often than anyone admits. */
    public void corrupt(String sku) {
        LegacyStockRecord r = rows.get(sku);
        rows.put(sku, new LegacyStockRecord(r.ITM_CD(), "12X", r.IN_STK_FLG(), r.ITM_STAT(), r.LST_CNT_DT(), r.WHSE_CD(), r.UOM()));
    }
}
