package com.jk.explore.acl.domain;

/** What the shop asks of an inventory system, in the shop's words. Whatever answers it is not the shop's concern. */
public interface InventoryGateway {
    StockLevel stockOf(String sku);
}
