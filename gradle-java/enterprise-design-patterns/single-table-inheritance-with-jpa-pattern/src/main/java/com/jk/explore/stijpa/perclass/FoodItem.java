package com.jk.explore.stijpa.perclass;

import jakarta.persistence.Entity;

/**
 * Its own table, with its own copy of the shared columns.
 */
@Entity
public class FoodItem extends CatalogItem {

    private String bestBefore;

    protected FoodItem() {
    }

    public FoodItem(String sku, String name, int pence, String bestBefore) {
        super(sku, name, pence);
        this.bestBefore = bestBefore;
    }
}
