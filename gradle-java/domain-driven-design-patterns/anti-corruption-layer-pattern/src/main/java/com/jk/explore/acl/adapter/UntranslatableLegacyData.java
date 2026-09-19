package com.jk.explore.acl.adapter;

/** The legacy system sent something that means nothing in the shop's terms. It stops here, with the sku named. */
public class UntranslatableLegacyData extends RuntimeException {
    public UntranslatableLegacyData(String sku, String problem) {
        super("legacy data for " + sku + ": " + problem);
    }
}
