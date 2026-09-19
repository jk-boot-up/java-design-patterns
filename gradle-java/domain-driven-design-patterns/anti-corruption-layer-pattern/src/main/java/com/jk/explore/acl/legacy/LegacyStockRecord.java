package com.jk.explore.acl.legacy;

/** A row from the old inventory system, exactly as it sends it: every value a string, every code a cryptic one. */
public record LegacyStockRecord(String ITM_CD, String QTY_ON_HND, String IN_STK_FLG, String ITM_STAT,
                                String LST_CNT_DT, String WHSE_CD, String UOM) {
}
