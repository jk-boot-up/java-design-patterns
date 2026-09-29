package com.jk.explore.stijpa.perclass;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Inheritance;
import jakarta.persistence.InheritanceType;

/**
 * Before: the same products with a table for every class (JPA's TABLE_PER_CLASS strategy).
 */
@Entity
@Inheritance(strategy = InheritanceType.TABLE_PER_CLASS)
public abstract class CatalogItem {

    @Id
    private String sku;
    private String name;
    private int pence;

    protected CatalogItem() {
    }

    protected CatalogItem(String sku, String name, int pence) {
        this.sku = sku;
        this.name = name;
        this.pence = pence;
    }

    public String getName() {
        return name;
    }
}
