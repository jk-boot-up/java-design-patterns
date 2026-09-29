package com.jk.explore.stijpa.perclass;

import jakarta.persistence.Entity;

/**
 * Its own table, with its own copy of the shared columns.
 */
@Entity
public class ElectronicsItem extends CatalogItem {

    private int warrantyYears;

    protected ElectronicsItem() {
    }

    public ElectronicsItem(String sku, String name, int pence, int warrantyYears) {
        super(sku, name, pence);
        this.warrantyYears = warrantyYears;
    }
}
